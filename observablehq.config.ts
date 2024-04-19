// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "YIMBY Melbourne Data",
  header: "<a href='https://www.yimby.melbourne/'><img src='https://assets-global.website-files.com/64a530aa67ffbab04c9c39ab/64b27aa3f510a34fa5003e6a_logo_inter.svg' height=50/></a>",
  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "Walkability",
      path: "/walkability",
    },
    {
      name: "Maximum distance to desired amenities",
      path: "/distance",
    },
    {
      name: "Permit analysis",
      path: "/permits",
    }
  ],

  // Some additional configuration options and their defaults:
  theme: "light", // try "light", "dark", "slate", etc.
  style: "theme-yimby-melbourne.css"
  // header: "", // what to show in the header (HTML)
  // footer: "Built with Observable.", // what to show in the footer (HTML)
  // toc: true, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // root: "docs", // path to the source root for preview
  // output: "dist", // path to the output root for build
};
