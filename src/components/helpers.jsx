// for the schedule
export function Label(props) {
  return (
    <span
      className="inline-block rounded-lg bg-red-200 w-auto text-xs md:text-sm px-2"
    >
      {props.type ? props.type + ":" : "Due:"} {props.children}
    </span>
  );
}

export function Badge(props) {
  if (!props.name) return <></>;
  return (
    <span
      className="inline-block rounded-lg bg-lightblue text-white w-auto text-xs md:text-sm px-2 mr-1"
    >
      {props.name}
    </span>
  );
}
