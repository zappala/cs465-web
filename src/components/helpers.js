export const formatSemester = (url) => {
  // the url is like /winter2024
  // directory is the first part after the leading slash
  console.log(url.url);
  const directory = url.split("/")[1];
  // find the year
  const year = directory.match(/\d+/);
  // find the semester
  let semester = directory.split(year)[0];
  // capitalize semester
  semester = semester.charAt(0).toUpperCase() + semester.slice(1);
  return semester + " " + year;
};
