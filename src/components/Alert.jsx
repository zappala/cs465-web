export default function Alert(props) {
  return (
    <div className="p-5 bg-yellow justify-center text-xl font-bold">
      {props.children}
    </div>
  );
}
