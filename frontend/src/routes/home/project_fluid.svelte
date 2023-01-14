<script>
	import { onMount } from 'svelte';

	let WebGLFluid;
	onMount(async () => {
		WebGLFluid = (await import('https://unpkg.com/webgl-fluid@0.3/dist/webgl-fluid.mjs')).default;
	});

	$: if (WebGLFluid) {
		console.log(WebGLFluid);
		WebGLFluid(document.querySelector('canvas'), {
			IMMEDIATE: false, // Whether to trigger multiple random splats when initialized
			TRIGGER: 'hover', // Can be change to 'click'

			SIM_RESOLUTION: 64, //128
			DYE_RESOLUTION: 256, //1024
			CAPTURE_RESOLUTION: 256, //512
			DENSITY_DISSIPATION: 1,
			VELOCITY_DISSIPATION: 0.1, //0.3
			PRESSURE: 0.8,
			PRESSURE_ITERATIONS: 20,

			CURL: 0.1, //30
			SPLAT_RADIUS: 1, //0.35
			SPLAT_FORCE: 6000,

			SHADING: true,
			COLORFUL: true,
			COLOR_UPDATE_SPEED: 10,
			PAUSED: false,

			BACK_COLOR: { r: 0, g: 0, b: 0 },
			TRANSPARENT: true,

			BLOOM: false,
			BLOOM_ITERATIONS: 8,
			BLOOM_RESOLUTION: 256,
			BLOOM_INTENSITY: 0.8,
			BLOOM_THRESHOLD: 0.6,
			BLOOM_SOFT_KNEE: 0.7,

			SUNRAYS: false,
			SUNRAYS_RESOLUTION: 196,
			SUNRAYS_WEIGHT: 1.0
		});
	}
</script>

<canvas />

<style>
	canvas {
		position: absolute;

		width: 100vw;
		height: 100vh;
	}
</style>
