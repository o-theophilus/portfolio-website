<script>
	import Content from '$lib/content.svelte';
	import Observe from '$lib/observe.svelte';
	import Cod from './welcome.cod.svelte';
</script>

<div id="scroll_1" />
<Content fit>
	<Observe let:intersecting>
		<div class="comp" class:intersecting>
			<div class="headline">Creating Engaging & Accessible Digital Experiences.</div>

			<div class="about">
				I'm <span class="bold"> Theophilus Ogbolu </span>
				, a designer and developer passionate about creating digital products that delight users. I blend
				design and technology to build intuitive, visually appealing experiences. With a focus on user-centric
				design, I strive to create solutions that are both functional and aesthetically pleasing.
			</div>

			<Cod />
		</div>
	</Observe>
</Content>

<style>
	.comp {
		margin-bottom: var(--sp5);
		
		position: relative;
		opacity: 0;
		transform: translate(0, -500px) scale(0);
	}
	
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	.headline {
		color: var(--ft1);
		font-size: 2.6rem;
		font-weight: 800;
		
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
