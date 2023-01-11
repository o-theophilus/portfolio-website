<script>
	import { page } from '$app/stores';
	import Content from '$lib/comp/content.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';

	let error = $page.error.message;
	export const data = '';
	export const form = '';
</script>

<Meta title={error} description={error.message} image="/site/akropol_001.jpg" />

<Content>
	<section>
		<div>
			<strong class="big">{$page.status}</strong>
			<br />
			{error}
		</div>
		<img src="/site/error.png" alt="error" />

		<Button href="/">Back to Home</Button>
	</section>
</Content>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap3);
	}
</style>
