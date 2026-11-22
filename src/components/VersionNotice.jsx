import { FiArrowRight, FiInfo, FiCheckCircle } from "react-icons/fi";

// A notice that links an original page and its updated version.
//
//   <VersionNotice link="/fall2026/notes/x-v2">Why it was updated.</VersionNotice>
//     on the original page: points to the updated version
//
//   <VersionNotice kind="original" link="/fall2026/notes/x">...</VersionNotice>
//     on the updated page: says it is the updated version, links the original
export default function VersionNotice({ kind = "updated", link, children }) {
  const updated = kind === "updated";
  // info: "note, there is a newer version"; check: "you are on the current one"
  const Icon = updated ? FiInfo : FiCheckCircle;
  const title = updated
    ? "An updated version of this page is available"
    : "This is the updated version of this page";
  const linkText = updated ? "Go to the updated version" : "See the original version";

  return (
    <aside
      className={
        "not-prose my-6 flex gap-4 rounded-lg border p-5 shadow-xs " +
        (updated
          ? "border-sky-200 bg-sky-50 border-l-4 border-l-sky-500"
          : "border-slate-200 bg-slate-50 border-l-4 border-l-slate-400")
      }
    >
      <Icon
        aria-hidden="true"
        className={"mt-1 h-6 w-6 shrink-0 " + (updated ? "text-sky-600" : "text-slate-500")}
      />
      <div className="text-base text-gray-800">
        <p className="font-semibold text-lg text-gray-900">{title}</p>
        {children && <div className="mt-1">{children}</div>}
        <a
          href={link}
          className={
            "mt-3 inline-flex items-center gap-1 rounded-sm px-3 py-1.5 text-sm font-semibold " +
            (updated
              ? "bg-sky-600 text-white hover:bg-sky-700"
              : "border border-slate-300 bg-white text-gray-800 hover:bg-slate-100")
          }
        >
          {linkText}
          <FiArrowRight aria-hidden="true" />
        </a>
      </div>
    </aside>
  );
}
