#!/usr/bin/python
import argparse
from glob import glob
import os, sys
from subprocess import call, Popen

OUTPUT_DIR = 'output'

def clean(output_dir):
    exts = ['.dvi', '.aux', '.blg', '.pdf', '.bcf', '.log', '.xml', '.bbl']
    for ext in exts:
        search_string = '%s/*%s'%(output_dir, ext)
        filenames = glob(search_string)
        for filename in filenames:
            os.remove(filename)

def make_pdf(output_dir, base_filename):
    pdf_cmd = ('pdflatex --output-directory=%s %s.tex'%(output_dir, base_filename))
    bibtex_cmd = ('bibtex %s/%s.aux'%(output_dir, base_filename))
    call(pdf_cmd.split(' '))
    call(bibtex_cmd.split(' '))

def view(output_dir, base_filename):
    pdf_view_cmd = 'evince %s/%s.pdf'%(output_dir, base_filename)
    Popen(pdf_view_cmd.split(' '))

def main(args):
    output_dir = args.output_dir if args.output_dir else OUTPUT_DIR
    if args.clean:
        clean(output_dir)
    if args.make:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        make_pdf(output_dir, args.base_filename)
    if args.view:
        view(output_dir, args.base_filename)
    return 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-dir')
    parser.add_argument('-m', '--make', action='store_true')
    parser.add_argument('-c', '--clean', action='store_true')
    parser.add_argument('-v', '--view', action='store_true')
    parser.add_argument('input_filename', nargs='?')

    args = parser.parse_args()
    if args.clean:
        main(args)
    elif args.make:
        if not args.input_filename or os.path.splitext(args.input_filename)[-1] != '.tex':
            print('Please enter a tex filename')
        else:
            if not os.path.exists(args.input_filename):
                print('File %s does not exist'%args.input_filename)
            else:
                args.base_filename = '.'.join(os.path.splitext(args.input_filename)[:-1])
                main(args)
    elif args.view:
        if not args.input_filename or os.path.splitext(args.input_filename)[-1] != '.pdf':
            print('Please enter a tex filename')
        else:
            args.base_filename = '.'.join(os.path.splitext(args.input_filename)[:-1])
            main(args)
        

