from frontier_taxonomy.textnorm import find_quote, normalize, quote_hash


def test_typography_and_whitespace_do_not_matter():
    text = "Claude “leads” 26%\nof Anthropic’s  AI R&D work — as of August."
    assert find_quote(text, 'Claude "leads" 26% of Anthropic\'s AI R&D work - as of August.')


def test_wording_matters():
    text = "Claude leads 26% of the work."
    assert find_quote(text, "Claude leads 30% of the work.") is None
    assert find_quote(text, "claude leads 26% of the work.") is None


def test_ellipsis_segments_must_appear_in_order():
    text = "First the plan was written. Then the grader was built. Last, it was run."
    assert find_quote(text, "the plan was written [...] it was run")
    assert find_quote(text, "it was run [...] the plan was written") is None


def test_empty_quote_is_never_found():
    assert find_quote("anything", "  ") is None
    assert find_quote("anything", "[...]") is None


def test_pdf_line_end_hyphenation():
    text = "the evalu-\nation was run"
    assert find_quote(text, "the evaluation was run")


def test_pdf_text_with_lost_word_spacing():
    text = "Thisincludesrewardhacking suchasincompleteimplementations"
    assert find_quote(text, "This includes reward hacking such as incomplete implementations")
    assert find_quote(text, "This includes reward hacking such as complete implementations") is None


def test_quote_hash_changes_with_the_quote():
    assert quote_hash("a b") == quote_hash(" a b ")
    assert quote_hash("a b") != quote_hash("a  b")
    assert normalize(" a \n b ") == "a b"
