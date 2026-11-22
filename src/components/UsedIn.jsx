import { FiCalendar } from "react-icons/fi";

// For the 2018-2023 course's shared pages: which semesters used this page,
// and under which number. Children are Markdown (links to the semesters).
//
//   <UsedIn>
//     [Fall 2018](/fall2018) to [Fall 2023](/fall2023), as Project 1
//   </UsedIn>
export default function UsedIn({ children }) {
  return (
    <aside className="not-prose my-6 flex gap-4 rounded-lg border border-slate-200 bg-slate-50 border-l-4 border-l-slate-400 p-4 text-base">
      <FiCalendar aria-hidden="true" className="mt-1 h-5 w-5 shrink-0 text-slate-500" />
      <div className="[&_a]:text-byu [&_a]:underline">
        <span className="font-bold">Used in: </span>
        {children}
      </div>
    </aside>
  );
}
