#!/usr/bin/env python2

import os
from os import path
from argparse import ArgumentParser
import api, fmt, visual, logic
import json

def ensure_dir(d):
    if not os.path.exists(d):
        os.mkdir(d)

def fetch_problems(args):
    workdir = args.workdir
    ensure_dir(workdir)

    snapshot_ref = api.latest_snapshot()
    snapshot_name = os.path.join(workdir, 'snapshot.json')
    snapshot = api.fetch_blob(snapshot_ref['snapshot_hash'])
    with open(snapshot_name, 'w') as f:
        f.write(snapshot)

    for p in json.loads(snapshot)['problems']:
        problem_dir = os.path.join(workdir, 'problem_{:05}'.format(p['problem_id']))
        ensure_dir(problem_dir)
        problem_name = os.path.join(problem_dir, 'problem.json')
        spec_name = os.path.join(problem_dir, 'spec.txt')
        spec = api.fetch_blob(p['problem_spec_hash'])
        p['spec'] = spec
        with open(spec_name, 'w') as f:
            f.write(spec)
        with open(problem_name, 'w') as f:
            f.write(json.dumps(p))
        print 'Problem: {}'.format(problem_name)

def push_solution(args):
    problem_file = path.join(args.problem_dir, 'problem.json')
    if not path.exists(args.problem_dir) or not path.exists(problem_file):
        raise 'Invalid problem path: {}'.format(args.problem_dir)
    problem = json.load(open(problem_file))
    solution = open(args.solution_file).read()
    solution_dir = path.join(args.problem_dir, args.name)
    ensure_dir(solution_dir)

    resp = api.push_solution(problem, solution)
    print resp

    with open(path.join(solution_dir, 'solution.txt'), 'w') as f:
        f.write(solution)

    with open(path.join(solution_dir, 'checker.json'), 'w') as f:
        json.dump(resp, f)

def show_problem(args):
    problem = open(path.join(args.problem_dir, 'spec.txt')).read()
    spec = fmt.parse_spec(problem)
    print "Polygons:", len(spec['polygons'])
    for point in spec['polygons'][0]:
        print "{},{}".format(point[0], point[1])

    shift = logic.detect_shift(spec['polygons'])
    print 'Shift: ', shift
    visual.show_skeleton(spec['edges'], shift)


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    fetch = subparsers.add_parser('fetch')
    fetch.add_argument('workdir')
    fetch.set_defaults(func=fetch_problems)

    solve = subparsers.add_parser('solution')
    solve.add_argument('problem_dir')
    solve.add_argument('solution_file')
    solve.add_argument('--name', default='manual')
    solve.set_defaults(func=push_solution)

    show = subparsers.add_parser('show')
    show.add_argument('problem_dir')
    show.set_defaults(func=show_problem)

    args = parser.parse_args()
    args.func(args)
