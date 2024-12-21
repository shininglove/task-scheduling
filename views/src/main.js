//@ts-ignore
import { createInertiaApp } from "@inertiajs/svelte";
import Layout from "./layouts/Layout.svelte";
import "./app.css";
import { mount } from "svelte";

createInertiaApp({
  //@ts-ignore
  resolve: (name) => {
    const allPages = import.meta.glob('./**/*.svelte', { eager: true })
    const page = allPages[`./pages/${name}.svelte`];
    const layout = page.layout
      ? (Array.isArray(page.layout) ? [Layout, ...page.layout] : [Layout, page.layout])
      : [Layout]
    return { default: page.default, layout: page.layout || layout }
  },

  //@ts-ignore
  setup({ el, App, props }) {
    mount(App, { target: el, props });
  },
});
