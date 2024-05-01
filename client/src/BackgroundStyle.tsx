const bgFilter = "rgb(255, 180, 89,0.5)";
const url = "d18xMDAwLGFyXzE2OjksY19maWxsLGdfYXV0byxlX3NoYXJwZW4=.jpeg";
const BGStyleMobile = {
  backgroundColor: bgFilter,
};

const BGStyleDesktop = {
  backgroundImage: `linear-gradient(${bgFilter}, ${bgFilter}),` + `url(${url})`,
  backgroundRepeat: "no-repeat",
  backgroundSize: "cover",
  backgroundPosition: "center",
  backgroundAttachment: "fixed",
};

function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent,
  );
}

function isFixedBackgroundSupported() {
  const testEl = document.createElement("div");
  testEl.style.backgroundAttachment = "fixed";
  return testEl.style.backgroundAttachment === "fixed";
}

const BGStyleFinal =
  !isMobile() && isFixedBackgroundSupported() ? BGStyleDesktop : BGStyleMobile;

// const BGStyleFinal = BGStyleDesktop;
export default BGStyleFinal;
