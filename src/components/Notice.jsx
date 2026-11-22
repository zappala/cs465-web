import { FiAlertTriangle, FiInfo } from "react-icons/fi";

// A standalone callout, styled like VersionNotice but without a link.
//
//   <Notice title="Update">Skip problem 5.</Notice>        // amber "note"
//   <Notice kind="info" title="Heads up">...</Notice>      // sky "info"
export default function Notice({ kind = "note", title = "Note", children }) {
  const note = kind === "note";
  const Icon = note ? FiAlertTriangle : FiInfo;

  return (
    <aside
      className={
        "not-prose my-6 flex gap-4 rounded-lg border p-5 shadow-xs " +
        (note
          ? "border-amber-200 bg-amber-50 border-l-4 border-l-amber-500"
          : "border-sky-200 bg-sky-50 border-l-4 border-l-sky-500")
      }
    >
      <Icon
        aria-hidden="true"
        className={"mt-1 h-6 w-6 shrink-0 " + (note ? "text-amber-600" : "text-sky-600")}
      />
      <div className="text-base text-gray-800">
        <p className="font-semibold text-lg text-gray-900">{title}</p>
        {children && <div className="mt-1 [&_a]:underline">{children}</div>}
      </div>
    </aside>
  );
}
