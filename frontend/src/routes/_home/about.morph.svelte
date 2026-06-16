<div class="cod">
	<svg viewBox="0 0 10362.15 9963.51" height="300px">
		<path
			d="M4606.59 1601.43c911.9,-2967.78 7556.53,-1925.37 5274.54,4277.67 -3053.05,8299 -13230.37,1915.54 -8757.61,-1458 1006.51,-869.66 2431.24,603.49 3483.06,-2819.67z"
		/>
	</svg>
	<div class="one"></div>
</div>

<style>
	.cod {
		position: relative;
		z-index: -1;
	}
	svg {
		position: absolute;
		right: 0;
		bottom: -100px;

		fill: color-mix(in srgb, #876145, transparent 95%);
	}

	.one {
		width: 180px;
		aspect-ratio: 1/1;
		border-radius: 50%;
		background-color: color-mix(in srgb, #876145, transparent 95%);

		position: absolute;
		right: 100px;
		bottom: -50px;

		animation: moveRight 30s cubic-bezier(0.42, 0, 0.58, 1) infinite;
	}

	@keyframes moveRight {
		0% {
			right: 50px;
			bottom: -25px;
		}
		20% {
			right: 100px;
			bottom: -50px;
		}
		40% {
			right: 75px;
			bottom: -10px;
		}
		60% {
			right: 125px;
			bottom: -60px;
		}
		80% {
			right: 150px;
			bottom: -75px;
		}
		100% {
			right: 50px;
			bottom: -25px;
		}
	}
</style>
