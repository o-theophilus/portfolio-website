<script>
	import Parallax from './hero.parallax.svelte';
	import Scroller from './scroller.svelte';
	import { Icon2 } from '$lib/macro';
</script>

<section>
	<Parallax />

	<div class="scroller">
		<Scroller query="#scroll_1" invert>
			<Icon2 icon="arrow_down" />
		</Scroller>
	</div>
</section>

<style>
	section {
		position: relative;
	}
	.scroller {
		position: absolute;
		width: 100%;
		bottom: 200px;

		display: flex;
		justify-content: center;
	}
</style>
