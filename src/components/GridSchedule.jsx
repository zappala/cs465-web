import { Label, Badge } from "./helpers.jsx";

import { load_yaml } from "./YamlLoader.js";

export default function GridSchedule(props) {
  const schedule = load_yaml("src/data" + props.prefix + "/schedule.yaml");

  // render units
  const render_units = (units) => {
    if (units === undefined) {
      console.log("WARNING: Units undefined");
      return <></>;
    }
    return (
      <>
        {units.map((unit, unit_index) => (
          <div key={unit_index}>
            <div className="bg-byu text-white text-center mb-1 p-2 break-words">
              {unit.title}
            </div>
            <div>{render_days(props.prefix, unit)}</div>
          </div>
        ))}
      </>
    );
  };

  // render days
  const render_days = (prefix, unit) => {
    if (unit.days === undefined) {
      console.log("WARNING: days undefined", unit.title);
      return <></>;
    }
    return <>{unit.days.map((day, index) => render_day(prefix, day, index))}</>;
  };

  // render a day or a separator
  const render_day = (prefix, day, index) => {
    if (day.separator) {
      return <></>;
    }
    if (day.holiday) {
      return (
        <div className="flex" key={index}>
          <div className="w-2/12 bg-gray-200 mb-1 mr-1 p-2">
            {day.day} {day.date}
          </div>
          <div className="w-10/12 bg-yellow-200 mb-1 mr-1 p-2">
            HOLIDAY - {day.holiday}
          </div>
        </div>
      );
    }
    if (day.exam) {
      return (
        <div className="flex" key={index}>
          <div className="w-2/12 bg-gray-200 mb-1 mr-1 p-2">
            {day.day} {day.date}
          </div>
          <div className="w-10/12 bg-red-200 mb-1 mr-1 p-2">{day.exam}</div>
        </div>
      );
    }
    return (
      <div className="flex" key={index}>
        <div className="w-2/12 bg-gray-200 mb-1 mr-1 p-2">
          {day.day} {day.date}
        </div>
        <div className="w-4/12 bg-gray-200 mb-1 mr-1 p-2">
          {render_lectures(prefix, day)}
        </div>
        <div className="w-3/12 bg-gray-200 mb-1 mr-1 p-2">
          {render_reading_or_readings(prefix, day)}
        </div>
        <div className="w-3/12 bg-gray-200 mb-1 mr-1 p-2">
          {render_project(prefix, day.project)}
        </div>
      </div>
    );
  };

  // render any/all lectures in a day
  const render_lectures = (prefix, day) => {
    if (!day.lectures) return <></>;
    if (day.lectures.constructor.name != "Array") return <></>;
    return (
      <ul>
        {day.lectures.map((lecture, lecture_index) =>
          render_lecture(prefix, lecture, lecture_index)
        )}
      </ul>
    );
  };

  // render an individual lecture
  const render_lecture = (prefix, lecture, index) => {
    if (!lecture.link) {
      return <li key={index}>{lecture.title}</li>;
    }
    let after_content = `after:content-[',_']`;
    let after_last_content = "last:after:content-['']";
    let target = "";
    let icon = <></>;
    if (lecture.type == "tab") {
      after_content = "after:content-['_↗,_']";
      after_last_content = "last:after:content-['_↗'] ";
      target = "_blank";
      icon = <></>;
    }
    if (lecture.type === "zip") {
      icon = <img className="w-5 inline" src="/icons/zip.png" />;
      after_content = `after:content-[',_']`;
      after_last_content = "last:after:content-['']";
      target = "";
      // icon = <Icon name="icon-park-outline:file-zip" />;
    }
    return (
      <li
        className={`inline ${after_content} ${after_last_content} after:text-xs`}
        key={index}
      >
        <a
          className="underline decoration-lightblue"
          href={prefix + "/" + lecture.link}
          target={target}
        >
          <Badge name={lecture.instructor} />
          {lecture.title} {icon}
        </a>
      </li>
    );
  };

  // render reading(s)
  const render_reading_or_readings = (prefix, day) => {
    if (day.reading) return <>{day.reading}</>;
    if (!day.readings) return <></>;
    if (day.readings.constructor.name != "Array") return <></>;
    return (
      <ul>
        {day.readings.map((reading, reading_index) =>
          render_reading(prefix, reading, reading_index)
        )}
      </ul>
    );
  };

  // render any/all guides in a day
  const render_reading = (prefix, reading, index) => {
    let after_content = `after:content-[',_']`;
    let after_last_content = "last:after:content-['']";
    let target = "";
    if (!reading.title) return <>{reading}</>;
    if (reading.link && reading.sections) {
      return (
        <li
          className={`inline ${after_content} ${after_last_content} after:text-xs`}
          key={index}
        >
          <a
            className="underline decoration-lightblue"
            href={reading.link}
            target={target}
          >
            {reading.title}
          </a>
          , {reading.sections}
        </li>
      );
    } else if (!reading.link) return <>{reading.title}</>;
  };

  // render a project
  const render_project = (prefix, project) => {
    if (!project) return <></>;
    let result = [];
    if (!project.link) result.push(project.title);
    else
      result.push(
        <a
          key="project"
          className="underline decoration-lightblue"
          href={prefix + "/" + project.link}
        >
          {project.title}
        </a>
      );
    if (project.due)
      result.push(
        <>
          {" "}
          <span>&nbsp;</span>
          <Label>{project.due}</Label>
        </>
      );
    return result;
  };

  // render the schedule
  return (
    <div className="mt-5 text-sm md:text-base">
      <div className="flex h-10 mb-1">
        <p className="w-2/12 p-2 font-bold">Day</p>
        <p className="w-4/12 p-2 font-bold">Topics</p>
        <p className="w-3/12 p-2 font-bold">Reading</p>
        <p className="w-3/12 p-2 font-bold">Assignments</p>
      </div>
      {render_units(schedule.units)}
    </div>
  );
}
