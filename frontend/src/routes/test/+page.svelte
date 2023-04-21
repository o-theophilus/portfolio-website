<script>
	import { _user, api_url } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button.svelte';

	// export let data;
	let user = {};
</script>

<Meta title={user.name} description="{user.name} profile" image="/site/home.jpg" />

<Content>
	<Button class="secondary" on:click={async () => {}}>Logout</Button>
</Content>

<style>
</style>
