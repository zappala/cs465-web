export default function Button(props) {
  return (
    <a
      href={props.link}
      className="not-prose inline-block bg-white hover:bg-sky-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow-lg no-underline"
    >
      {props.children}
    </a>
  );
}
