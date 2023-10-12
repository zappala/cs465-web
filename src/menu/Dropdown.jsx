const Dropdown = ({ submenus, dropdown }) => {
  let base = "hidden";
  if (dropdown) base = "";
  return (
    <div className={base + " bg-gray-800 text-white p-3 lg:absolute"}>
      <ul className="border-l-2 border-l-white pl-2">
        {submenus.map((submenu, index) => (
          <li key={index} className="py-2 px-1">
            <a className="text-white hover:underline" href={submenu.url}>
              {submenu.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dropdown;
