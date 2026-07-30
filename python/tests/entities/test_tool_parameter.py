from pathlib import Path

from dify_plugin.core.utils.yaml_loader import load_yaml_file
from dify_plugin.entities.model.provider import FormOption
from dify_plugin.entities.tool import ToolParameter


def test_tool_parameter_reset_on_change_yaml_round_trip(tmp_path: Path):
    tool_yaml = tmp_path / "tool.yaml"
    tool_yaml.write_text(
        """
parameters:
  - name: a
    type: select
    form: form
    label:
      en_US: A
    human_description:
      en_US: A
    options:
      - value: foo
        label:
          en_US: Foo
  - name: b
    type: dynamic-select
    form: form
    label:
      en_US: B
    human_description:
      en_US: B
    reset_on_change:
      - a
""".strip(),
        encoding="utf-8",
    )

    declaration = load_yaml_file(str(tool_yaml))
    parameters = [ToolParameter(**parameter) for parameter in declaration["parameters"]]

    assert parameters[1].reset_on_change == ["a"]
    assert parameters[1].model_dump(mode="json")["reset_on_change"] == ["a"]


def test_tool_parameter_reset_on_change_defaults_to_empty_list():
    parameter = ToolParameter(
        name="legacy",
        type="string",
        form="form",
        label={"en_US": "Legacy"},
        human_description={"en_US": "Legacy parameter"},
    )

    assert parameter.reset_on_change == []
    assert parameter.model_dump(mode="json")["reset_on_change"] == []


def test_option_level_show_on_is_unchanged():
    option = FormOption(
        value="foo",
        label={"en_US": "Foo"},
        show_on=[{"variable": "mode", "value": "advanced"}],
    )

    serialized_option = option.model_dump(mode="json")

    assert serialized_option["show_on"] == [{"variable": "mode", "value": "advanced"}]
    assert "reset_on_change" not in serialized_option
