from hitori_generator import Generator
from argparse import ArgumentParser


def generate(n: int, output_file: str) -> None:
    if n < 3 or n > 8:
        print("It isn't valid size")
        exit(4)
    generator = Generator(n)
    data = generator.generate()
    lines = map(lambda x: ' '.join(map(str, x)), data)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    p = ArgumentParser()
    p.add_argument('filename', type=str, help='Path to output file')
    p.add_argument('-s', "--size", type=int, default=3, help='Generate SxS field. size must be in [3, 8]. Default is 3')

    args = p.parse_args()
    generate(args.size, args.filename)


if __name__ == '__main__':
    main()
