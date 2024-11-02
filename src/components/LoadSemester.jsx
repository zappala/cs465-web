import { load_yaml } from "./YamlLoader.js";

export default function LoadSemester(semester) {
  const menu = load_yaml("src/data" + semester + "/menu.yaml");

  return menu.menu;
}
