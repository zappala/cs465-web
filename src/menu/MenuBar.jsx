// Much of the responsive menu is based on https://awadieudonne.com/blog/How-to-create-a-responsive-hamburger-navigation-menu-ReactJS-and-Styled-Components

import Menu from "./Menu.jsx";

const MenuBar = ({ prefix, items, open }) => {
  let base =
    "flex flex-nowrap flex-col list-none bg-gray-800 fixed top-0 right-0 m-0 h-full overflow-y-auto w-72 pt-8 pl-8 lg:flex-row lg:h-auto lg:p-0 lg:bg-blue-100 lg:static lg:w-auto lg:transform-none";
  if (!open) {
    base = base + " translate-x-full";
  } else {
    base = base + " transform-none";
  }
  return (
    <div className={base}>
      {items.map((menu, index) => {
        return <Menu prefix={prefix} items={menu} key={index} />;
      })}
    </div>
  );
};

export default MenuBar;
