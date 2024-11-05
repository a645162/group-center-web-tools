from cairosvg import svg2eps


def convert_svg_to_eps(svg_file, eps_file):
    """将 SVG 文件转换为 EPS 文件"""
    with open(svg_file, 'rb') as svg_input:
        svg_data = svg_input.read()
        svg2eps(bytestring=svg_data, write_to=eps_file)


if __name__ == "__main__":
    svg_file = "input.svg"
    eps_file = "output.eps"

    convert_svg_to_eps(svg_file, eps_file)
    print(f"SVG 文件已成功转换为 EPS 文件：{eps_file}")
