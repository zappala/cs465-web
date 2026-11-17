// Much of the responsive menu is based on https://awadieudonne.com/blog/How-to-create-a-responsive-hamburger-navigation-menu-ReactJS-and-Styled-Components

import Menu from "./Menu.jsx";

const MenuBar = ({ prefix, items, open }) => {
  let base =
    "flex flex-nowrap flex-col list-none bg-gray-800 fixed top-0 right-0 m-0 h-full overflow-y-auto w-72 pt-8 pl-8 lg:flex-row lg:h-auto lg:p-0 lg:bg-blue-100 lg:static lg:w-auto lg:transform-none";
  // When closed on small screens, the menu slides off-screen and is made
  // invisible so its links are not reachable with the keyboard; on large
  // screens it is always shown inline.
  if (!open) {
    base = base + " translate-x-full invisible lg:visible";
  } else {
    base = base + " transform-none";
  }
  return (
    <ul id="site-menu" className={base}>
      {items.map((menu, index) => {
        return <Menu prefix={prefix} items={menu} key={index} />;
      })}
    </ul>
  );
};

export default MenuBar;
