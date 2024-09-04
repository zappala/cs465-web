export function Cards(props) {
  return (
    <div className="w-full sm:flex sm:flex-wrap lg:w-[150%] sm:max-w-screen">
      {props.children}
    </div>
  );
}

export function Card(props) {
  return (
    <div className="w-full md:flex shadow-lg p-3 border-t border-gray-200 dark:bg-gray-900 mb-3">
      {props.image && (
        <img
          className="w-28 h-28 rounded-full mr-8 ml-5"
          src={"/images/" + props.image}
          alt={"Photo of " + props.name}
        />
      )}
      <div className="md:mt-10 mr-5 ml-5">{Instructor(props)}</div>

      <div className="text-gray-700 text-sm ml-5 mr-5">{props.children}</div>
    </div>
  );
}

export function Instructor(props) {
  return (
    <>
      <div className="text-gray-900 dark:text-gray-300 font-bold text-xl mb-0">
        {props.name}
      </div>
      <div>
        {props.email && (
          <span className="font-bold text-sm">{props.email}</span>
        )}

        {props.office && (
          <span>
            <br />
            <span className="font-bold text-sm">{props.office}</span>
          </span>
        )}

        {props.hours && (
          <span className="text-sm">
            <br />
            <span className="font-bold">Office Hours: </span>
            {props.hours}
          </span>
        )}
        <br />

        {props.schedule && (
          <span className="text-sm">
            <span className="font-bold">Office Hours: </span>
            <a href={props.schedule}>schedule an appointment</a>
          </span>
        )}
      </div>
    </>
  );
}
