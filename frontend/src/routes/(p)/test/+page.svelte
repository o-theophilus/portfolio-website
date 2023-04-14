<script>
	import { _user, api_url } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Content from '$lib/comp/content.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';

	// export let data;
	let user = {};
</script>

<Meta title={user.name} description="{user.name} profile" image="/site/home.jpg" />

<Content>
	<Button
		class="secondary"
		on:click={async () => {
		}}>Logout</Button
	>
</Content>

<style>
</style>
