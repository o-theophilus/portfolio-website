<script>
	import Observe from '$lib/observe.svelte';
	import Content from '$lib/content.svelte';
</script>

<Content fit>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			As a Designer & Developer, I enjoy bridging the gap between engineering and design — combining
			my technical knowledge with my keen eye for design to create a beautiful product. My goal is
			to always build applications that are scalable and efficient under the hood while providing
			engaging, pixel-perfect user experiences.

			<br />
			<br />

			I've always been fascinated by crafting digital experiences that people love. From building my
			own projects to contributing to open-source communities, I enjoy the thrill of turning ideas
			into reality. I believe in the power of collaboration and learning from others, which has
			shaped my approach to design and development.

			<br />
			<br />
			When I am not designing or programming, you can find me playing music, exploring my surroundings,
			or spending time with my family and friends. I believe that a balanced and fulfilling life is essential
			to creative inspiration and success.

			<div class="cod">
				<svg viewBox="0 0 10362.15 9963.51" height="300px">
					<path
						d="M4606.59 1601.43c911.9,-2967.78 7556.53,-1925.37 5274.54,4277.67 -3053.05,8299 -13230.37,1915.54 -8757.61,-1458 1006.51,-869.66 2431.24,603.49 3483.06,-2819.67z"
					/>
				</svg>
				<div class="one" />
			</div>
		</div>
	</Observe>
</Content>

<style>
	.observe {
		margin: var(--sp5) 0;
		position: relative;
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: all 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	.cod {
		position: relative;
		z-index: -1;
	}
	svg {
		position: absolute;
		right: 0;
		bottom: -100px;

		fill: color-mix(in srgb, var(--cl6), transparent 95%);
	}

	.one {
		width: 180px;
		aspect-ratio: 1/1;
		border-radius: 50%;
		background-color: color-mix(in srgb, var(--cl6), transparent 95%);

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
