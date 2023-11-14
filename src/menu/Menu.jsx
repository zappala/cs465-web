import { useState } from "react";
import Dropdown from "./Dropdown";
import { FaCaretRight, FaCaretDown } from "react-icons/fa";

const Menu = ({ prefix, items }) => {
  const [dropdown, setDropdown] = useState(false);
  return (
    <li className="menu-items">
      {items.submenu ? (
        <>
          <button
            className="text-white lg:text-default lg:px-5 text-xl"
            type="button"
            aria-haspopup="menu"
            aria-expanded={dropdown ? "true" : "false"}
            onClick={() => setDropdown((prev) => !prev)}
          >
            <div className="flex">
              {items.title}

              {dropdown ? (
                <FaCaretDown className="mt-1" />
              ) : (
                <FaCaretRight className="mt-1" />
              )}
            </div>
          </button>
          <Dropdown prefix={prefix} submenus={items.submenu} dropdown={dropdown} />
        </>
      ) : (
        <a
          className="text-white mt-4 text-xl lg:text-default lg:px-5 lg:mt-0 hover:underline"
          href={prefix + items.url}
        >
          {items.title}
        </a>
      )}
    </li>
  );
};

export default Menu;
