from nonstory import TemplateBuilder

def test_template():
    builder = TemplateBuilder()
    template = builder.build("${Who} eat the apple?\nAt ${When}")
    assert (len(template) == 2 and
             template["${Who}"] == "${Who} eat the apple?"
              and template["${When}"] == "At ${When}")