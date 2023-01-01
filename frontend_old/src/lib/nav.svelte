<script>
	import { browser } from '$app/env';
	// fix nav header blink

	import Link from './navBtn.svelte';
</script>

{#if browser}
	<nav>
		<Link name={'home'} link={''} />
		<Link name={'project'} />
		<Link name={'blog'} />
	</nav>
{/if}

<style>
	@media screen and (min-width: 900px) {
		nav {
			display: flex;

			height: 100%;
			width: 100%;
			max-width: 500px;

			margin-left: auto;
		}
	}
</style>
