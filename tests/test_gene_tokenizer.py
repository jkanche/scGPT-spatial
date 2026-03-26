"""Tests for GeneVocab to verify functional equivalence after removing torchtext."""

import json
import tempfile
from pathlib import Path

from scgpt_spatial.tokenizer.gene_tokenizer import GeneVocab


def test_from_list():
    vocab = GeneVocab(["GeneA", "GeneB", "GeneC"])
    assert len(vocab) == 3
    assert "GeneA" in vocab
    assert "GeneD" not in vocab


def test_from_list_with_specials_first():
    vocab = GeneVocab(["GeneA", "GeneB"], specials=["<pad>", "<cls>"], special_first=True)
    assert vocab["<pad>"] == 0
    assert vocab["<cls>"] == 1
    assert "GeneA" in vocab
    assert "GeneB" in vocab


def test_from_list_with_specials_last():
    vocab = GeneVocab(["GeneA", "GeneB"], specials=["<pad>", "<cls>"], special_first=False)
    assert "GeneA" in vocab
    assert "GeneB" in vocab
    assert vocab["<pad>"] > vocab["GeneB"]
    assert vocab["<cls>"] > vocab["<pad>"]


def test_from_dict():
    token2idx = {"<pad>": 0, "<cls>": 1, "GeneA": 2, "GeneB": 3}
    vocab = GeneVocab.from_dict(token2idx)
    assert len(vocab) == 4
    assert vocab["<pad>"] == 0
    assert vocab["GeneA"] == 2


def test_from_file_json():
    token2idx = {"<pad>": 0, "<cls>": 1, "<eoc>": 2, "GeneA": 3}
    with tempfile.TemporaryDirectory() as d:
        vocab_file = Path(d) / "vocab.json"
        vocab_file.write_text(json.dumps(token2idx))
        vocab = GeneVocab.from_file(vocab_file)
    assert len(vocab) == 4
    assert vocab["<pad>"] == 0
    assert vocab["GeneA"] == 3
    assert "<cls>" in vocab


def test_unknown_token_fallback():
    token2idx = {"<pad>": 0, "<cls>": 1, "GeneA": 2}
    vocab = GeneVocab.from_file(Path(tempfile.mktemp(suffix=".json"))) if False else GeneVocab.from_dict(token2idx)
    vocab.set_default_token("<pad>")
    assert vocab["UNKNOWN_GENE"] == vocab["<pad>"]


def test_batch_lookup():
    vocab = GeneVocab(["GeneA", "GeneB", "GeneC"], specials=["<pad>"], special_first=True)
    indices = vocab(["<pad>", "GeneA", "GeneC"])
    assert indices == [vocab["<pad>"], vocab["GeneA"], vocab["GeneC"]]


def test_insert_token():
    vocab = GeneVocab([])
    vocab.insert_token("<pad>", 0)
    vocab.insert_token("GeneA", 1)
    assert vocab["<pad>"] == 0
    assert vocab["GeneA"] == 1
    assert len(vocab) == 2


def test_append_token():
    vocab = GeneVocab(["GeneA"])
    n = len(vocab)
    vocab.append_token("GeneB")
    assert "GeneB" in vocab
    assert vocab["GeneB"] == n
