<script>
	import Parallax from './hero.parallax.svelte';
	import Scroller from '$lib/scroller.svelte';
	import Icon from '$lib/icon.svelte';
</script>

<section>
	<Parallax />

	<div class="scroller">
		<Scroller query="#scroll_1" invert>
			<Icon icon="arrow_downward" />
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
