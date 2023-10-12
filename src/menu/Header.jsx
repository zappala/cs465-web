export default function Header(props) {
  return (
    <div class="text-xl pt-15 md:text-2xl font-bold">
      <a href="/">{props.semester}</a>
    </div>
  );
}
