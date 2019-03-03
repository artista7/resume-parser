from utils.pdf_utils import convert_pdf
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
import networkx as nx
from constants import SECTION_TITLES
from modules.extraction.common_extraction import extract_name, extract_email, \
                                                    extract_phone_num

class PDFParser:
    """
        :: DOCSTRING ::
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.xml = convert_pdf(self.file_name, format='xml')  + "</pages>"
        self.root = ET.fromstring(self.xml)
        self._parse_xml()
        self.name = extract_name(self.sections[0]['text'])
        self.email = extract_email(self.sections[0]['text'])
        self.phone = extract_phone_num(self.sections[0]['text'])

    def _extract_textline_properties(self, item):
        """
        """
        attrib = item.attrib
        reslist = list(item.iter())
        text = ''.join([element.text for element in reslist])
        properties = [element.attrib for element in reslist]
        property_dict = defaultdict(list)
        for property in properties:
            for key in property:
                property_dict[key].append(property[key])
        property_dict = dict(property_dict)
        property_dict.pop("bbox")
        for key in property_dict:
            val = Counter(list(property_dict[key])).most_common(1)[0][0]
            property_dict[key] = val
        property_dict["text"] = text
        return property_dict

    def _is_a_bullet(self, text):
        pass

    def is_a_section_breaker(self, text):
        # Simple rules as number of words and content of words
        pass

    def _find_vertical_nearest_line(self, y ):
        ys = self.sorted_bbox['y1']
        correct_idx = None
        for idx in range(len(ys)):
            if ys[idx][0] >= y:
                break
        idx = idx - 1
        return idx

    def _find_horizontal_nearest_line(self, x ):
        pass

    def _get_section_candidates(self):
        pass

    def _bbidx2idx(self, idx, axis):
        return self.sorted_bbox[axis][idx][1]

    def _check_merge_via_tokenization(self, text1, text2):
        text2 = nltk.word_tokenize(text)[0]


    def _match_lines(self, line1, line2):
        # TODO Need to improve this bit
        # This logic depends on paper size
        # First level check font size
        match = False
        if abs(float(line2['size']) - float(line1['size'])) < .5:
            # Second level check (first char is small)
            text1 = line1['text'].strip()
            text2 = line2['text'].strip()

            if not( text1) or not(text2):
                match =False
            elif  not text2[0].isalpha():
                match = False
            elif text2[0].islower():
                match = True
            else:
                match = True
        return match

    def _merge_lines(self):
        merged = []
        graph = nx.Graph()
        for idx in self.properties:
            # Get coordinates
            item = self.properties[idx]
            x1, y1, x2, y2 = map(float, item['bbox'].split(','))
            # Find nearest y index
            found_match = False
            y_idx = self._find_vertical_nearest_line(y1)
            prop_idx = None
            while True:
                # Find idx corresponding to bbox
                prop_idx = self._bbidx2idx(y_idx, 'y1')
                # Check if y is beyond a threshold in which case break
                if abs(self.bbox['y1'][prop_idx] - y1) > 25:
                    break
                # Check if x is within a threshold if yes match
                if abs(self.bbox['x1'][prop_idx] - x1) < 20:
                    found_match = True
                    break
                y_idx -= 1
            if found_match:
                check_matched = self._match_lines(self.properties[idx], self.properties[prop_idx])
                if check_matched:
                    merged.append((idx, prop_idx))
                    graph.add_edge(idx, prop_idx)
                    graph.add_node(idx)
        cc = list(nx.connected_components(graph))
        return cc


    def _get_sections(self):
        """
            Extraction lines which are sections

            :returns:
        """
        candidates = []
        font_counter = Counter()
        for idx in  self.properties:
            item = self.properties[idx]
            if len(item['text'].split()) < 5 and any(i.lower() in item['text'].lower() for i in SECTION_TITLES):
                font_counter[item['size']] += 1
                candidates.append(idx)
        common_font = font_counter.most_common(1)[0][0]
        candidates = [i for i in candidates if self.properties[i]['size'] == common_font]
        return candidates

    def _parse_xml(self):
        """
            Parse the
        """
        self.properties = {}
        self.bbox = {'x1': [] , 'y1':[], 'x2':[], 'y2':[]}
        textlines = self.root.findall('page/textbox/textline')
        textlines = sorted(textlines, key= lambda x: -float(x.attrib['bbox'].split(',')[3]))


        for idx, item in enumerate(textlines):
            self.properties[idx] = self._extract_textline_properties(item)
            self.properties[idx]['bbox'] = item.attrib['bbox']
            bbox = item.attrib['bbox'].split(',')
            self.bbox['x1'].append(float(bbox[0]))
            self.bbox['x2'].append(float(bbox[2]))
            self.bbox['y1'].append(float(bbox[1]))
            self.bbox['y2'].append(float(bbox[3]))

        self.sorted_bbox = {'x1': [] , 'y1':[], 'x2':[], 'y2':[]}
        for key in self.sorted_bbox:
            temp = [(val, idx) for idx, val in enumerate(self.bbox[key])]
            temp = sorted(temp, key=lambda x: x[0])
            self.sorted_bbox[key] = temp

        # Merge different lines which are broken into different lines
        self.merged_components = self._merge_lines()

        # Extract different Sections from Resume
        self.sections = []
        section_start_idx = self._get_sections()
        section_end_idx = section_start_idx[1:] + [max(list(self.properties.keys()))]
        self.sections.append({
                                'start': 0,
                                'end': section_start_idx[0],
                                'title': '~NAME_SECTION~',
                                'text' : ''.join([self.properties[i]['text']
                                                for i in range(0, section_start_idx[0])])
                            })
        for span_start, span_end in zip(section_start_idx, section_end_idx):
            self.sections.append({
                                    'start': span_start,
                                    'end': span_end,
                                    'title': self.properties[span_start]['text'].strip(),
                                    'text' : ''.join([self.properties[i]['text']
                                                          for i in range(span_start, span_end)])
                                })
