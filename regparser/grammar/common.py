#vim: set encoding=utf-8
import string

from pyparsing import alphanums, CaselessLiteral, Literal, OneOrMore, Optional
from pyparsing import Regex, Suppress, Word, WordEnd, WordStart

def WordBoundaries(grammar):
    return WordStart(alphanums) + grammar + WordEnd(alphanums)

# Atomic components; probably shouldn't use these directly
lower_p = (
        Suppress("(") 
        + Word(string.ascii_lowercase, max=1).setResultsName("level1") 
        + Suppress(")"))
digit_p = (
        Suppress("(") 
        + Word(string.digits).setResultsName("level2") 
        + Suppress(")"))
roman_p = (
        Suppress("(") 
        + Word("ivxlcdm").setResultsName("level3") + 
        Suppress(")"))
upper_p = (
        Suppress("(") 
        + Word(string.ascii_uppercase).setResultsName("level4") 
        + Suppress(")"))
em_digit_p = (
        Suppress(Regex(r"\(<E[^>]*>"))
        + Word(string.digits).setResultsName("level5")
        + Suppress("</E>)"))

part = Word(string.digits).setResultsName("part")

section = Word(string.digits).setResultsName("section")

appendix_letter = Word(string.ascii_uppercase).setResultsName("letter")

section_marker = Suppress(Regex(u"§|Section|section")) 
section_markers = Suppress(Regex(u"§§|Sections|sections"))

paragraph_marker = Suppress("paragraph")
paragraph_markers = Suppress("paragraphs")

part_marker = Suppress("part")
part_markers = Suppress("parts")

through = WordBoundaries(CaselessLiteral("through"))

conj_phrases = (
        Regex(",|and|or") 
        + Optional("and") 
        + Optional("or")
)

appendix_marker = Suppress("Appendix")

interpretation_marker = (
        Suppress("Supplement")
        + Suppress("I")
        + Suppress("to")
)

#   Minimally composed
depth4_p = upper_p + Optional(em_digit_p)
depth3_p = roman_p + Optional(depth4_p)
depth2_p = digit_p + Optional(depth3_p)
depth1_p = lower_p + Optional(depth2_p)

any_depth_p = (
        depth1_p.setResultsName("depth1_p") 
        | depth2_p.setResultsName("depth2_p") 
        | depth3_p.setResultsName("depth3_p") 
        | depth4_p.setResultsName("depth4_p")
        | em_digit_p.setResultsName("depth5_p"))

any_p = lower_p | digit_p | roman_p | upper_p | em_digit_p

part_section = part + Suppress(".") + section

marker_part_section = section_marker + part_section
marker_part_sections = (
        section_markers 
        + part_section 
        + OneOrMore(
            conj_phrases 
            + part_section.setResultsName("s_tail", listAllMatches=True)
        )
)

marker_paragraph = paragraph_marker + depth1_p

marker_part = part_marker + part

marker_appendix = (
        appendix_marker 
        + appendix_letter 
        + Literal("to")
        + marker_part
)

appendix_shorthand = (
        appendix_letter 
        + Suppress("-") 
        + section
        + Optional(lower_p)
)

marker_interpretation = interpretation_marker + marker_part
