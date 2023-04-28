<script>
	import { _user, module } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Delete from './slug.comment.item__menu__delete__.svelte';
	import Report from './slug.comment.item__menu__report__.svelte';

	export let comment;
</script>

<div class="content">
	<strong class="big">Comment</strong>
	{#if comment.user_key == $_user.key}
		<br /><br />
		<Button
			name="Delete"
			class="wide"
			on:click={() => {
				$module = {
					module: Delete,
					comment_key: comment.key
				};
			}}
		/>
	{:else}
		<br /><br />
		<Button
			name="Report"
			class="wide"
			on:click={() => {
				$module = {
					module: Report,
					owner_key: comment.key,
					owner_type: 'comment'
				};
			}}
		/>
		<!-- <br /><br />
		<Button
			name="Report User"
			class="wide"
			on:click={() => {
				$module = {
					module: Report,
					owner_key: $_user.key,
					owner_type: 'user'
				};
			}}
		/> -->
	{/if}
</div>

<style>
	.content {
		padding: var(--gap3);
	}
</style>
