#!/usr/bin/env python
import argparse
import os
import docker
import shutil


class DockerShare(object):
    def __init__(self, args):
        if args.machine:
            self.cli = docker.from_env(assert_hostname=False)
        else:
            self.cli = docker.Client(base_url=args.socket, tls=False, version='0.21')

    def get(self, args):
        resp = [line for line in self.cli.pull(args.tag, stream=True)]
        if args.debug:
            for line in resp:
                print(line.decode('utf-8'))
        ctnr = self.cli.create_container(args.tag, 'true')
        strm, stat = self.cli.get_archive(ctnr, '/payload')
        tarfile = '{0}.tar'.format(args.output)
        temp = open(os.path.abspath(tarfile), 'w+b')
        for line in strm:
            temp.write(line)
        temp.close()
        print('Wrote .tar of file to: {0}'.format(tarfile))

    def put(self, args):
        shutil.copyfile(os.path.abspath(args.file), '/tmp/payload')
        filename = '/tmp/Dockerfile'
        temp = open(filename, 'w+b')
        dockerfile = '''
        FROM scratch
        COPY payload /payload
        '''
        temp.write(dockerfile.encode('utf-8'))
        temp.close()
        resp = [line for line in self.cli.build(path='/tmp/', rm=True, tag=args.tag)]
        if args.debug:
            for line in resp:
                print(line.decode('utf-8'))
        os.remove(filename)
        os.remove('/tmp/payload')
        resp = [line for line in self.cli.push(args.tag, stream=True)]
        if args.debug:
            for line in resp:
                print(line.decode('utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Store and retrieve files on Docker Hub!')
    ap.add_argument('--debug', action='store_true', help="Debugging output")
    gp = ap.add_mutually_exclusive_group()
    gp.add_argument('--socket', '-s', type=str, default='unix://var/run/docker.sock', help='Path to Docker socket')
    gp.add_argument('--machine', '-m', action='store_true', help='Use Docker machine?')
    sp = ap.add_subparsers(dest='cmd')
    sp.required = True
    put = sp.add_parser('put')
    put.add_argument('--file', '-f', type=str, required=True, help='File to put')
    put.add_argument('--tag', '-t', type=str, required=True, help='Tag to put')
    get = sp.add_parser('get')
    get.add_argument('--tag', '-t', required=True, type=str, help='Tag to get')
    get.add_argument('--output', '-o', required=True, type=str, help='File to write')
    args = ap.parse_args()
    ds = DockerShare(args)
    getattr(ds, args.cmd)(args)


if __name__ == '__main__':
    main()
