const csrf = document.querySelector("meta[name=csrf]").content;
async function post(url) {
  const res = await fetch(url, {method: "POST", headers: {"X-CSRFToken": csrf}});
  if (res.redirected) { location.href = res.url; return null; }
  return res.ok ? res.json() : null;
}
document.addEventListener("click", async e => {
  const like = e.target.closest(".like"), fol = e.target.closest(".follow");
  if (like) {
    const d = await post(like.dataset.url); if (!d) return;
    like.classList.toggle("on", d.liked); like.querySelector("span").textContent = d.count;
    like.classList.remove("pop"); void like.offsetWidth; like.classList.add("pop");
  } else if (fol) {
    const d = await post(fol.dataset.url); if (!d) return;
    fol.classList.toggle("on", d.following); fol.textContent = d.following ? "Unfollow" : "Follow";
    const c = document.getElementById("followers-count"); if (c) c.textContent = d.followers;
  }
});
// Composer: live character count, enable button only when there is text, Ctrl+Enter to send.
document.querySelectorAll(".composer").forEach(f => {
  const t = f.querySelector("textarea"), n = f.querySelector(".count"), b = f.querySelector(".bottom button");
  if (!t) return;
  const sync = () => { const left = 280 - t.value.length; n.textContent = left; n.classList.toggle("warn", left < 20); b.disabled = !t.value.trim(); };
  t.addEventListener("input", sync);
  t.addEventListener("keydown", e => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey) && t.value.trim()) f.submit(); });
  sync();
});
