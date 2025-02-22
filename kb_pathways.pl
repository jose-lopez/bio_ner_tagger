base([
event('IMPORTIN',association,'CXCR4'),
event('CXCR4',association,'JAK3'),
event('JAK3',association,'STAT'),
event('STAT',positive_correlation,'COVID-19'),
event('COCAINE',association,'CXCR4'),
event('CALCIUM',association,'CXCR4'),
event('TYROSINE',association,'CXCR4'),
event('ARGININE',association,'CXCR4'),
event('Aspartic Acid',association,'CXCR4'),
event('Glutamic Acid',association,'CXCR4'),
event('WATER',association,'CXCR4'),
event('PLERIXAFOR',association,'CXCR4'),
event('LIPIDS',association,'CXCR4'),
event('Hyaluronic Acid',association,'CXCR4'),
event('TESTOSTERONE',association,'CXCR4'),
event('MANGANESE',association,'CXCR4'),
event('DOXORUBICIN',association,'CXCR4'),
event('ISOPROTERENOL',association,'CXCR4'),
event('baohuoside I',association,'CXCR4'),
event('METAPERIODATE',association,'CXCR4'),
event('Polyglutamic Acid',association,'CXCR4'),
event('carbon-11 methionine',association,'CXCR4'),
event('ICARITIN',association,'CXCR4'),
event('FLAVONOIDS',association,'CXCR4'),
event('GEMCITABINE',association,'CXCR4'),
event('STAT',association,'PIAS3'),
event('PIAS3',association,'HLA-C'),
event('HLA-C',association,'CD4'),
event('CD4',positive_correlation,'COVID-19'),
event('CD4',negative_correlation,'COVID-19'),
event('CD4',association,'INTERFERON'),
event('INTERFERON',association,'ACE2'),
event('ACE2',positive_correlation,'COVID-19'),
event('INTERFERON',association,'PIAS4'),
event('PIAS4',association,'ACE2'),
event('PIAS3',association,'INTERFERON'),
event('INTERFERON',association,'CD4'),
event('INTERFERON',association,'CIITA'),
event('CIITA',association,'CD4'),
event('ACE2',association,'CD4'),
event('INTERFERON',association,'ORF6'),
event('ORF6',association,'CD4'),
event('PIAS3',association,'CD4'),
event('STAT',association,'CD4'),
event('JAK3',association,'CD4'),
event('CIITA',association,'STAT'),
event('INTERFERON',association,'STAT'),
event('ORF6',association,'STAT'),
event('CD4',association,'STAT'),
event('CXCR4',association,'CD4'),
event('INTERFERON',association,'JAK3'),
event('CD4',association,'JAK3'),
event('ZILEUTON',association,'ACE2'),
event('SULFUR',association,'ACE2'),
event('BA 1',association,'ACE2'),
event('CHLOROQUINE',association,'ACE2'),
event('HYDROXYCHLOROQUINE',association,'ACE2'),
event('12-Hydroxy-5 8 10 14-eicosatetraenoic Acid',association,'ACE2'),
event('Cholic Acid',association,'ACE2'),
event('ERGOTHIONEINE',association,'ACE2'),
event('GLYCYLPHENYLALANINE',association,'ACE2'),
event('Deoxycholic Acid',association,'ACE2'),
event('INDOLE',association,'ACE2'),
event('CP protocol',association,'ACE2'),
event('1 2-oleoylphosphatidylcholine',association,'ACE2'),
event('M-2 protocol',association,'ACE2'),
event('TEBUTHIURON',association,'ACE2'),
event('STAT',association,'CXCR4'),
event('CXCR4',positive_correlation,'COVID-19'),
event('CXCR4',negative_correlation,'COVID-19'),
event('JAK3',association,'CXCR4'),
event('CCR5',bind,'CD4'),
event('MICA',association,'CD4'),
event('CCR5',association,'CD4'),
event('CXCR4',bind,'CD4'),
event('INDOLINE',bind,'CD4'),
event('CARBAMAZEPINE',association,'CD4'),
event('VANCOMYCIN',association,'CD4'),
event('IPILIMUMAB',association,'CD4'),
event('COPPER-64',association,'CD4'),
event('THYROXINE',association,'CD4'),
event('Phorbol Esters',association,'CD4'),
event('Guanosine Diphosphate',association,'CD4'),
event('DOPAMINE',association,'CCR5'),
event('TYROSINE',association,'CCR5'),
event('WATER',association,'CCR5'),
event('ABACAVIR',association,'CCR5'),
event('LICOPYRANOCOUMARIN',association,'CCR5'),
event('METALS',association,'CCR5'),
event('CCR5',association,'STAT')
]).