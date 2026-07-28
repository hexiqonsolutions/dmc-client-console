export const dashboardNav = [
  {
    href: "/dashboard",
    label: "Dashboard",
    exact: true,
  },
  {
    href: "/dashboard/clients",
    label: "Clients",
    exact: false,
  },
  {
    href: "/dashboard/projects",
    label: "Projects",
    exact: false,
  },
  {
    href: "/dashboard/settings",
    label: "Settings",
    exact: false,
  },
] as const;

export function isNavActive(pathname: string, href: string, exact?: boolean) {
  if (exact) {
    return pathname === href;
  }
  return pathname === href || pathname.startsWith(`${href}/`);
}
