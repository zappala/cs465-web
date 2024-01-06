// for the schedule
export function Label(props) {
  return (
    <button
      disabled
      className="rounded-lg bg-red-200 w-auto text-xs md:text-sm px-2"
    >
      {props.type ? props.type + ":" : "Due:"} {props.children}
    </button>
  );
}

export function Badge(props) {
  if (!props.name) return <></>;
  return (
    <button
      disabled
      className="rounded-lg bg-lightblue text-white w-auto text-xs md:text-sm px-2 mr-1"
    >
      {props.name}
    </button>
  );
}
