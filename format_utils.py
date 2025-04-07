def format_paragraph(text, max_length=40):
    if not isinstance(text, str):
        return text  # Si ce n'est pas une chaîne, on ne fait rien

    sentences = text.split(".")
    formatted = ""
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > max_length:
            formatted += sentence + ".\n"
        else:
            formatted += sentence + ". "
    return formatted.strip()
