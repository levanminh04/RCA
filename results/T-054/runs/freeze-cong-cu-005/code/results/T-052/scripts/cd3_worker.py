"""C-d3 ở tiến trình riêng; chỉ nhận đầu vào phi nhãn đã seal của M1."""
import sys
from fractions import Fraction
from common import read,dump
from m1 import doi_chung

if __name__ == '__main__':
    data = read(sys.argv[1])
    scores = {entity: Fraction(*pair) for entity,pair in data['diem'].items()}
    print(dump(doi_chung.cd3(data['canh'],scores,data['dich'])))
