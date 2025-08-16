<script>
	import { Content } from '$lib/layout';
	import { Observe } from '$lib/macro';
	import Morph from './about.morph.svelte';
</script>

<div id="scroll_1"></div>
<Content --content-height="100%">
	<Observe let:intersecting>
		<div class="comp" class:intersecting>
			<div class="headline">Creating Engaging & Accessible Digital Experiences.</div>

			<div class="about">
				I'm <span class="bold"> Theophilus Ogbolu </span>
				, a designer and developer passionate about creating digital products that delight users. I blend
				design and technology to build intuitive, visually appealing experiences. With a focus on user-centric
				design, I strive to create solutions that are both functional and aesthetically pleasing.
			</div>

			<Morph />
		</div>
	</Observe>
</Content>

<style>
	.comp {
		position: relative;
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition:
			opacity,
			transform 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);
	}

	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	.headline {
		color: var(--ft1);
		font-size: 2.6rem;
		font-weight: 800;
		line-height: 120%;

		max-width: 400px;
		transition: color var(--trans);
	}

	.about {
		margin-top: var(--sp3);
		font-size: 1.4rem;
		max-width: 490px;
	}

	.bold {
		font-weight: 800;
	}
</style>
