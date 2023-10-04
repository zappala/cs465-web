export default function Alert(props) {
    return (
      <div className="p-5 bg-yellow justify-center text-2xl font-bold">
        {props.children}
      </div>
    );
  }