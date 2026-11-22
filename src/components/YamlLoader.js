import fs from "fs";
import { load } from "js-yaml";

export const load_yaml = (filename) => {
  try {
    let fileContents = fs.readFileSync(filename, "utf8");
    let data = load(fileContents);
    return data;
  } catch (e) {
    console.log(e);
    return {};
  }
};
