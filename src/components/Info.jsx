export default function Info(props) {
  return (
    <div className="block max-w-sm p-6 bg-sky-50 border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
      <h5 className="font-playfair font-bold mb-2 text-2xl text-gray-900 dark:text-white">
        {props.title}
      </h5>
      <p className="font-normal text-gray-700 dark:text-gray-400">
        {props.children}
      </p>
    </div>
  );
}
