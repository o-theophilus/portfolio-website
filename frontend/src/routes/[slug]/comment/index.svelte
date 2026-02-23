<script>
	import { app, module,scroll } from '$lib/store.svelte.js';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Login } from '$lib/auth';
	import { Button, FoldButton, RoundButton } from '$lib/button';
	import { PageNote } from '$lib/info';
	import { Dropdown, Pagination } from '$lib/input';
	import { Icon, Spinner } from '$lib/macro';
	import Add from './_add.svelte';
	import Control from './one.control.svelte';
	import One from './one.svelte';

	let { post, comment_resp, loading } = $props();

	let comments = $derived(comment_resp.comments);
	let total_comment = $derived(comment_resp.total_comment);
	let total_page = $derived(comment_resp.total_page);
	let order_by = $derived(comment_resp.order_by);
	let searchParams = $derived(comment_resp.searchParams);

	let open = $derived(comments?.length > 0);

	const update = (a, b, c) => {
		comments = a;
		total_comment = b;
		total_page = c;
	};

	export const load = async () => {
		loading = true;

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/${post.key}/comments?${new URLSearchParams(searchParams).toString()}`,
			{
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			comments = resp.comments;
		}

		loading = false;
		scroll("#comment_section")
	};
</script>

<div class="line space" id="comment_section">
	<div class="line">
		<span class="page_title">
			{#if total_comment > 0}
				{total_comment}
			{/if}
			Comment{#if total_comment > 1}s{/if}
		</span>
		<Spinner active={loading} size="20" />
	</div>

	{#if !loading}
		<FoldButton
			{open}
			onclick={() => {
				open = !open;
			}}
		/>
	{/if}
</div>

{#if open && !loading}
	<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if comments?.length > 1}
			<Dropdown
				--select-height="10"
				--select-padding-x="0"
				--select-font-size="0.8rem"
				--select-background-color="transparent"
				--select-background-color-hover="transparent"
				--select-color-hover="var(--ft1)"
				--select-outline-color="transparent"
				list={order_by}
				icon="arrow-down-narrow-wide"
				icon2="chevron-down"
				bind:value={searchParams.order}
				onchange={(v) => {
					searchParams.page_no = 1;
					load();
				}}
			/>
		{/if}

		{#each comments as comment (comment.key)}
			<div class="comment" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				<div class="main">
					<One {comment}></One>
					<Control {comment} {post} {searchParams} {update}>
						{#snippet reply()}
							<RoundButton
								icon="reply"
								onclick={() => module.open(Add, { comment, post, searchParams, update })}
							/>
						{/snippet}
					</Control>
				</div>
				{#each comment.replies as reply (reply.key)}
					<div class="reply" animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
						<One comment={reply}></One>
						<Control comment={reply} {post} {searchParams} {update}></Control>
					</div>
				{/each}
			</div>
		{:else}
			<PageNote>
				<Icon icon="message-circle-off" size="50" />
				No comment
			</PageNote>
		{/each}

		<Pagination
			{total_page}
			bind:value={searchParams.page_no}
			ondone={(v) => {
				load();
			}}
		></Pagination>
	</div>
{/if}

<div class="button">
	{#if app.login}
		<Button
			icon="message-circle-plus"
			onclick={() => module.open(Add, { post, update, searchParams })}
		>
			Add comment
		</Button>
	{:else}
		<Button icon="log-in" onclick={() => module.open(Login)}>Login to add comment</Button>
	{/if}
</div>

<style>
	.comment {
		margin-top: 8px;

		border-radius: 8px;
		overflow: hidden;
		outline: 1px solid var(--ol);
		outline-offset: -1px;
	}

	.main {
		padding: 16px;
		background-color: var(--bg3);
	}
	.reply {
		border-top: 1px solid var(--ol);
		padding: 16px;
		background-color: var(--bg2);
	}

	.button {
		margin: 16px 0;
	}
</style>
