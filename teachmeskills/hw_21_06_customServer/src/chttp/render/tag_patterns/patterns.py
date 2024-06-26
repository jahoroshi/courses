patterns = (
    (r'{%\s*extend\s+([^\s%]+)\s*%}', '{% block extend %}'),
)

base_tags = (
    '{% extend block %}'
)