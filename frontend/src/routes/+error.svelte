<script>
	import { page } from '$app/stores';
	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

	let error = $page.error.message;
	export const data = '';
	export const form = '';
</script>

<Meta title={error} description={error.message} />

<Content>
	<br />
	<br />
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
<br />
<br />

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--gap3);
	}
</style>
