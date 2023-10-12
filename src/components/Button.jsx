export default function Button(props) {
  return (
    <form action={props.link}>
      <button
        type="submit"
        class="bg-white hover:bg-sky-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow-lg"
      >
        {props.children}
      </button>
    </form>
  );
}
