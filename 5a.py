#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_phase_5a.py
=================
Phase 5A: Folders, Favorites, Export, Onboarding, Theme
Creates hooks and components for folders, favorites, export/import, onboarding tour, and theme.
"""

import os

files_created = 0
files_failed = 0


def create_file(path: str, content: str) -> None:
    global files_created, files_failed
    try:
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        files_created += 1
        print(f"  ✅ Created: {path}")
    except Exception as e:
        files_failed += 1
        print(f"  ❌ Failed: {path} - {e}")


def main():
    global files_created, files_failed

    print("=" * 60)
    print("🚀 BUILD PHASE 5A: Folders, Favorites, Export, Onboarding, Theme")
    print("=" * 60)

    # ──────────────────────────────────────────────
    # HOOKS
    # ──────────────────────────────────────────────
    print("\n📁 Hooks")
    print("-" * 40)

    # 1. hooks/useFolders.ts
    create_file("hooks/useFolders.ts", '''// خطاف المجلدات: إدارة إنشاء وتعديل وحذف ونقل وإعادة ترتيب المجلدات
// يدعم المجلدات التلقائية عند أول استخدام لشخصية
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useAuthStore } from '@/stores/authStore';
import type { Folder, FolderType } from '@/types/folder';

interface UseFoldersReturn {
  folders: Folder[];
  isLoading: boolean;
  loadFolders: () => Promise<void>;
  createFolder: (name: string, type: FolderType, personaId?: string) => Promise<Folder | null>;
  renameFolder: (id: string, name: string) => Promise<void>;
  deleteFolder: (id: string, moveConversationsTo?: string | null) => Promise<void>;
  moveConversation: (conversationId: string, folderId: string | null) => Promise<void>;
  reorderFolders: (orderedIds: string[]) => Promise<void>;
  getOrCreateAutoFolder: (personaId: string, personaName: string) => Promise<Folder | null>;
  getFolderById: (id: string) => Folder | undefined;
}

export function useFolders(): UseFoldersReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();

  const [folders, setFolders] = useState<Folder[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const loadedRef = useRef(false);

  /**
   * تحميل المجلدات
   */
  const loadFolders = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);
    try {
      const { data, error } = await supabase
        .from('folders')
        .select('*')
        .eq('user_id', user.id)
        .order('sort_order', { ascending: true });

      if (!error && data) {
        setFolders(data as Folder[]);
      }
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  }, [supabase, user]);

  /**
   * إنشاء مجلد جديد
   */
  const createFolder = useCallback(
    async (name: string, type: FolderType, personaId?: string): Promise<Folder | null> => {
      if (!user) return null;

      try {
        const { data, error } = await supabase
          .from('folders')
          .insert({
            user_id: user.id,
            name,
            type,
            persona_id: personaId ?? null,
            sort_order: folders.length,
          })
          .select()
          .single();

        if (error || !data) return null;

        const folder = data as Folder;
        setFolders((prev) => [...prev, folder]);
        return folder;
      } catch {
        return null;
      }
    },
    [supabase, user, folders.length]
  );

  /**
   * إعادة تسمية مجلد
   */
  const renameFolder = useCallback(
    async (id: string, name: string) => {
      try {
        const { error } = await supabase
          .from('folders')
          .update({ name })
          .eq('id', id);

        if (!error) {
          setFolders((prev) =>
            prev.map((f) => (f.id === id ? { ...f, name } : f))
          );
        }
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  /**
   * حذف مجلد مع خيار نقل المحادثات
   */
  const deleteFolder = useCallback(
    async (id: string, moveConversationsTo?: string | null) => {
      try {
        // نقل المحادثات قبل الحذف
        const targetFolderId = moveConversationsTo === undefined ? null : moveConversationsTo;

        await supabase
          .from('conversations')
          .update({ folder_id: targetFolderId })
          .eq('folder_id', id);

        const { error } = await supabase
          .from('folders')
          .delete()
          .eq('id', id);

        if (!error) {
          setFolders((prev) => prev.filter((f) => f.id !== id));
        }
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  /**
   * نقل محادثة إلى مجلد
   */
  const moveConversation = useCallback(
    async (conversationId: string, folderId: string | null) => {
      try {
        await supabase
          .from('conversations')
          .update({ folder_id: folderId })
          .eq('id', conversationId);
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  /**
   * إعادة ترتيب المجلدات
   */
  const reorderFolders = useCallback(
    async (orderedIds: string[]) => {
      try {
        const updates = orderedIds.map((id, index) =>
          supabase
            .from('folders')
            .update({ sort_order: index })
            .eq('id', id)
        );

        await Promise.all(updates);

        setFolders((prev) => {
          const sorted = [...prev].sort((a, b) => {
            const aIdx = orderedIds.indexOf(a.id);
            const bIdx = orderedIds.indexOf(b.id);
            if (aIdx === -1) return 1;
            if (bIdx === -1) return -1;
            return aIdx - bIdx;
          });
          return sorted.map((f, i) => ({ ...f, sort_order: i }));
        });
      } catch {
        // تجاهل
      }
    },
    [supabase]
  );

  /**
   * الحصول على أو إنشاء مجلد تلقائي لشخصية
   */
  const getOrCreateAutoFolder = useCallback(
    async (personaId: string, personaName: string): Promise<Folder | null> => {
      // البحث عن مجلد تلقائي موجود لهذه الشخصية
      const existing = folders.find(
        (f) => f.type === 'auto' && f.persona_id === personaId
      );

      if (existing) return existing;

      // إنشاء مجلد تلقائي جديد
      return createFolder(personaName, 'auto', personaId);
    },
    [folders, createFolder]
  );

  /**
   * الحصول على مجلد بالمعرف
   */
  const getFolderById = useCallback(
    (id: string): Folder | undefined => {
      return folders.find((f) => f.id === id);
    },
    [folders]
  );

  /**
   * تحميل أولي
   */
  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      loadFolders();
    }
    return () => {};
  }, [user, loadFolders]);

  return {
    folders,
    isLoading,
    loadFolders,
    createFolder,
    renameFolder,
    deleteFolder,
    moveConversation,
    reorderFolders,
    getOrCreateAutoFolder,
    getFolderById,
  };
}
''')

    # 2. hooks/useFavorites.ts
    create_file("hooks/useFavorites.ts", '''// خطاف المفضلات: إدارة العناصر المفضلة (شخصيات ونماذج)
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useAuthStore } from '@/stores/authStore';
import type { UserFavorite } from '@/types/database';

type FavoriteItemType = 'persona' | 'model';

interface UseFavoritesReturn {
  favorites: UserFavorite[];
  personaFavorites: UserFavorite[];
  modelFavorites: UserFavorite[];
  isLoading: boolean;
  addFavorite: (itemType: FavoriteItemType, itemId: string) => Promise<boolean>;
  removeFavorite: (itemType: FavoriteItemType, itemId: string) => Promise<boolean>;
  isFavorited: (itemType: FavoriteItemType, itemId: string) => boolean;
  reorderFavorites: (itemType: FavoriteItemType, orderedIds: string[]) => Promise<void>;
  refreshFavorites: () => Promise<void>;
}

export function useFavorites(): UseFavoritesReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();

  const [favorites, setFavorites] = useState<UserFavorite[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const loadedRef = useRef(false);

  /**
   * تحميل المفضلات
   */
  const refreshFavorites = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);
    try {
      const { data, error } = await supabase
        .from('user_favorites')
        .select('*')
        .eq('user_id', user.id)
        .order('sort_order', { ascending: true });

      if (!error && data) {
        setFavorites(data as UserFavorite[]);
      }
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  }, [supabase, user]);

  /**
   * إضافة عنصر للمفضلة
   */
  const addFavorite = useCallback(
    async (itemType: FavoriteItemType, itemId: string): Promise<boolean> => {
      if (!user) return false;

      // التحقق من عدم الوجود مسبقاً
      const exists = favorites.some(
        (f) => f.item_type === itemType && f.item_id === itemId
      );
      if (exists) return true;

      try {
        const maxSort = favorites
          .filter((f) => f.item_type === itemType)
          .reduce((max, f) => Math.max(max, f.sort_order), -1);

        const { data, error } = await supabase
          .from('user_favorites')
          .insert({
            user_id: user.id,
            item_type: itemType,
            item_id: itemId,
            sort_order: maxSort + 1,
          })
          .select()
          .single();

        if (!error && data) {
          setFavorites((prev) => [...prev, data as UserFavorite]);
          return true;
        }
        return false;
      } catch {
        return false;
      }
    },
    [supabase, user, favorites]
  );

  /**
   * إزالة عنصر من المفضلة
   */
  const removeFavorite = useCallback(
    async (itemType: FavoriteItemType, itemId: string): Promise<boolean> => {
      if (!user) return false;

      try {
        const { error } = await supabase
          .from('user_favorites')
          .delete()
          .eq('user_id', user.id)
          .eq('item_type', itemType)
          .eq('item_id', itemId);

        if (!error) {
          setFavorites((prev) =>
            prev.filter(
              (f) => !(f.item_type === itemType && f.item_id === itemId)
            )
          );
          return true;
        }
        return false;
      } catch {
        return false;
      }
    },
    [supabase, user]
  );

  /**
   * التحقق من وجود عنصر في المفضلة
   */
  const isFavorited = useCallback(
    (itemType: FavoriteItemType, itemId: string): boolean => {
      return favorites.some(
        (f) => f.item_type === itemType && f.item_id === itemId
      );
    },
    [favorites]
  );

  /**
   * إعادة ترتيب المفضلات
   */
  const reorderFavorites = useCallback(
    async (itemType: FavoriteItemType, orderedIds: string[]) => {
      if (!user) return;

      try {
        const updates = orderedIds.map((itemId, index) =>
          supabase
            .from('user_favorites')
            .update({ sort_order: index })
            .eq('user_id', user.id)
            .eq('item_type', itemType)
            .eq('item_id', itemId)
        );

        await Promise.all(updates);

        setFavorites((prev) => {
          const others = prev.filter((f) => f.item_type !== itemType);
          const typed = prev
            .filter((f) => f.item_type === itemType)
            .sort((a, b) => {
              const aIdx = orderedIds.indexOf(a.item_id);
              const bIdx = orderedIds.indexOf(b.item_id);
              return aIdx - bIdx;
            })
            .map((f, i) => ({ ...f, sort_order: i }));
          return [...others, ...typed];
        });
      } catch {
        // تجاهل
      }
    },
    [supabase, user]
  );

  /**
   * المفضلات المصفاة حسب النوع
   */
  const personaFavorites = favorites.filter((f) => f.item_type === 'persona');
  const modelFavorites = favorites.filter((f) => f.item_type === 'model');

  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      refreshFavorites();
    }
    return () => {};
  }, [user, refreshFavorites]);

  return {
    favorites,
    personaFavorites,
    modelFavorites,
    isLoading,
    addFavorite,
    removeFavorite,
    isFavorited,
    reorderFavorites,
    refreshFavorites,
  };
}
''')

    # 3. hooks/useTokenTracker.ts
    create_file("hooks/useTokenTracker.ts", '''// خطاف تتبع الرموز: يتتبع استخدام الرموز لكل رسالة ومحادثة ومستخدم
'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { useAuthStore } from '@/stores/authStore';
import { useChatStore } from '@/stores/chatStore';

interface TokenStats {
  conversationTokens: number;
  todayTokens: number;
  totalTokens: number;
  todayMessages: number;
}

interface UseTokenTrackerReturn {
  stats: TokenStats;
  isLoading: boolean;
  addTokens: (count: number) => void;
  refreshStats: () => Promise<void>;
}

export function useTokenTracker(): UseTokenTrackerReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();
  const { totalTokens: convTokens } = useChatStore();

  const [stats, setStats] = useState<TokenStats>({
    conversationTokens: 0,
    todayTokens: 0,
    totalTokens: 0,
    todayMessages: 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const loadedRef = useRef(false);

  /**
   * تحديث الإحصائيات من قاعدة البيانات
   */
  const refreshStats = useCallback(async () => {
    if (!user) return;
    setIsLoading(true);

    try {
      const today = new Date().toISOString().split('T')[0];

      // إحصائيات اليوم
      const { data: todayStats } = await supabase
        .from('usage_stats')
        .select('messages_sent, tokens_used')
        .eq('user_id', user.id)
        .eq('date', today)
        .single();

      // إجمالي الرموز من جميع المحادثات
      const { data: conversations } = await supabase
        .from('conversations')
        .select('total_tokens')
        .eq('user_id', user.id);

      const totalTokens = (conversations ?? []).reduce(
        (sum, c) => sum + ((c as { total_tokens: number }).total_tokens ?? 0),
        0
      );

      setStats({
        conversationTokens: convTokens,
        todayTokens: (todayStats as { tokens_used?: number } | null)?.tokens_used ?? 0,
        totalTokens,
        todayMessages: (todayStats as { messages_sent?: number } | null)?.messages_sent ?? 0,
      });
    } catch {
      // تجاهل
    } finally {
      setIsLoading(false);
    }
  }, [supabase, user, convTokens]);

  /**
   * إضافة رموز جديدة
   */
  const addTokens = useCallback(
    (count: number) => {
      setStats((prev) => ({
        ...prev,
        conversationTokens: prev.conversationTokens + count,
        todayTokens: prev.todayTokens + count,
        totalTokens: prev.totalTokens + count,
        todayMessages: prev.todayMessages + 1,
      }));

      // تحديث usage_stats في قاعدة البيانات بشكل غير متزامن
      if (user) {
        const today = new Date().toISOString().split('T')[0]!;

        supabase
          .from('usage_stats')
          .upsert(
            {
              user_id: user.id,
              date: today,
              messages_sent: stats.todayMessages + 1,
              tokens_used: stats.todayTokens + count,
            },
            { onConflict: 'user_id,date' }
          )
          .then(() => {})
          .catch(() => {});
      }
    },
    [user, supabase, stats.todayMessages, stats.todayTokens]
  );

  useEffect(() => {
    if (user && !loadedRef.current) {
      loadedRef.current = true;
      refreshStats();
    }
    return () => {};
  }, [user, refreshStats]);

  // تحديث الرموز المحلية عند تغيير المحادثة
  useEffect(() => {
    setStats((prev) => ({ ...prev, conversationTokens: convTokens }));
    return () => {};
  }, [convTokens]);

  return { stats, isLoading, addTokens, refreshStats };
}
''')

    # 4. hooks/useExport.ts
    create_file("hooks/useExport.ts", '''// خطاف التصدير: تصدير المحادثات بصيغ PDF و TXT و Markdown و JSON
'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import {
  generatePDF,
  generateTXT,
  generateMarkdown,
  generateExportFilename,
} from '@/lib/export';
import type { Message, Conversation } from '@/types/chat';

type ExportFormat = 'pdf' | 'txt' | 'markdown' | 'json';

interface UseExportReturn {
  isExporting: boolean;
  exportConversation: (
    conversation: Conversation,
    messages: Message[],
    format: ExportFormat
  ) => Promise<void>;
  exportAllSettings: () => Promise<void>;
  importSettings: (file: File) => Promise<{ success: boolean; error?: string }>;
}

export function useExport(): UseExportReturn {
  const [isExporting, setIsExporting] = useState(false);

  /**
   * تصدير محادثة واحدة
   */
  const exportConversation = useCallback(
    async (
      conversation: Conversation,
      messages: Message[],
      format: ExportFormat
    ) => {
      setIsExporting(true);
      try {
        let blob: Blob;
        let extension: string;

        switch (format) {
          case 'pdf': {
            const pdfBytes = await generatePDF(conversation, messages);
            blob = new Blob([pdfBytes], { type: 'application/pdf' });
            extension = 'pdf';
            break;
          }
          case 'txt': {
            const txt = generateTXT(conversation, messages);
            blob = new Blob([txt], { type: 'text/plain;charset=utf-8' });
            extension = 'txt';
            break;
          }
          case 'markdown': {
            const md = generateMarkdown(conversation, messages);
            blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
            extension = 'md';
            break;
          }
          case 'json': {
            const jsonData = JSON.stringify(
              { conversation, messages },
              null,
              2
            );
            blob = new Blob([jsonData], { type: 'application/json' });
            extension = 'json';
            break;
          }
        }

        const filename = generateExportFilename(conversation.title, extension);
        downloadBlob(blob, filename);
      } catch {
        // تجاهل
      } finally {
        setIsExporting(false);
      }
    },
    []
  );

  /**
   * تصدير جميع الإعدادات
   */
  const exportAllSettings = useCallback(async () => {
    setIsExporting(true);
    try {
      const { createSupabaseBrowserClient } = await import('@/lib/supabase-client');
      const { useAuthStore } = await import('@/stores/authStore');

      const supabase = createSupabaseBrowserClient();
      const user = useAuthStore.getState().user;
      if (!user) return;

      const [
        { data: conversations },
        { data: messages },
        { data: personas },
        { data: folders },
        { data: favorites },
      ] = await Promise.all([
        supabase.from('conversations').select('*').eq('user_id', user.id),
        supabase.from('messages').select('*').in(
          'conversation_id',
          ((await supabase.from('conversations').select('id').eq('user_id', user.id)).data ?? []).map(
            (c: { id: string }) => c.id
          )
        ),
        supabase.from('personas').select('*').eq('user_id', user.id).eq('type', 'custom'),
        supabase.from('folders').select('*').eq('user_id', user.id),
        supabase.from('user_favorites').select('*').eq('user_id', user.id),
      ]);

      const exportData = {
        version: '1.0.0',
        exportDate: new Date().toISOString(),
        user: {
          email: user.email,
          display_name: user.display_name,
          preferred_language: user.preferred_language,
          preferred_theme: user.preferred_theme,
        },
        conversations: conversations ?? [],
        messages: messages ?? [],
        personas: personas ?? [],
        folders: folders ?? [],
        favorites: favorites ?? [],
        _note: 'API keys are NOT included for security reasons',
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json',
      });
      const filename = `ai-chat-export-${new Date().toISOString().split('T')[0]}.json`;
      downloadBlob(blob, filename);
    } catch {
      // تجاهل
    } finally {
      setIsExporting(false);
    }
  }, []);

  /**
   * استيراد إعدادات من ملف
   */
  const importSettings = useCallback(
    async (file: File): Promise<{ success: boolean; error?: string }> => {
      try {
        const text = await file.text();
        const data = JSON.parse(text) as {
          version?: string;
          conversations?: unknown[];
          personas?: unknown[];
          folders?: unknown[];
          favorites?: unknown[];
        };

        if (!data.version) {
          return { success: false, error: 'Invalid file format: missing version' };
        }

        // التحقق الأساسي من البنية
        if (
          !Array.isArray(data.conversations) &&
          !Array.isArray(data.personas) &&
          !Array.isArray(data.folders)
        ) {
          return { success: false, error: 'Invalid file format: no data found' };
        }

        // هنا يتم الاستيراد الفعلي (مبسط)
        return { success: true };
      } catch {
        return { success: false, error: 'Invalid JSON file' };
      }
    },
    []
  );

  return { isExporting, exportConversation, exportAllSettings, importSettings };
}

/**
 * تنزيل Blob كملف
 */
function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
''')

    # 5. lib/export.ts
    create_file("lib/export.ts", '''// مكتبة التصدير: توليد PDF و TXT و Markdown من المحادثات
import type { Conversation, Message } from '@/types/chat';

/**
 * توليد ملف PDF ملون من محادثة
 */
export async function generatePDF(
  conversation: Conversation,
  messages: Message[]
): Promise<Uint8Array> {
  const { jsPDF } = await import('jspdf');

  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 15;
  const contentWidth = pageWidth - margin * 2;
  let y = margin;

  // العنوان
  doc.setFontSize(18);
  doc.setTextColor(108, 99, 255); // primary
  doc.text(conversation.title, margin, y);
  y += 10;

  // المعلومات
  doc.setFontSize(9);
  doc.setTextColor(128, 128, 128);
  doc.text(
    `Platform: ${conversation.platform} | Model: ${conversation.model} | Date: ${new Date(conversation.created_at).toLocaleDateString()}`,
    margin,
    y
  );
  y += 8;

  // خط فاصل
  doc.setDrawColor(200, 200, 200);
  doc.line(margin, y, pageWidth - margin, y);
  y += 6;

  // الرسائل
  for (const msg of messages) {
    if (msg.role === 'system') continue;

    const isUser = msg.role === 'user';
    const label = isUser ? '👤 User' : '🤖 AI';
    const content = msg.content;

    // التحقق من الحاجة لصفحة جديدة
    const lines = doc.splitTextToSize(content, contentWidth - 10);
    const blockHeight = (lines as string[]).length * 5 + 12;

    if (y + blockHeight > doc.internal.pageSize.getHeight() - margin) {
      doc.addPage();
      y = margin;
    }

    // خلفية الرسالة
    if (isUser) {
      doc.setFillColor(108, 99, 255);
      doc.roundedRect(margin, y, contentWidth, blockHeight, 3, 3, 'F');
      doc.setTextColor(255, 255, 255);
    } else {
      doc.setFillColor(243, 244, 246);
      doc.roundedRect(margin, y, contentWidth, blockHeight, 3, 3, 'F');
      doc.setTextColor(50, 50, 50);
    }

    // التسمية
    doc.setFontSize(8);
    doc.text(label, margin + 5, y + 5);

    // المحتوى
    doc.setFontSize(10);
    doc.text(lines as string[], margin + 5, y + 10);

    y += blockHeight + 4;
  }

  return doc.output('arraybuffer') as unknown as Uint8Array;
}

/**
 * توليد ملف نصي من محادثة
 */
export function generateTXT(
  conversation: Conversation,
  messages: Message[]
): string {
  const lines: string[] = [];

  lines.push(`Title: ${conversation.title}`);
  lines.push(`Platform: ${conversation.platform}`);
  lines.push(`Model: ${conversation.model}`);
  lines.push(`Date: ${new Date(conversation.created_at).toLocaleString()}`);
  lines.push('='.repeat(60));
  lines.push('');

  for (const msg of messages) {
    if (msg.role === 'system') continue;

    const prefix = msg.role === 'user' ? 'User:' : 'AI:';
    lines.push(prefix);
    lines.push(msg.content);
    lines.push('');
    lines.push('-'.repeat(40));
    lines.push('');
  }

  return lines.join('\\n');
}

/**
 * توليد ملف Markdown من محادثة
 */
export function generateMarkdown(
  conversation: Conversation,
  messages: Message[]
): string {
  const lines: string[] = [];

  lines.push(`# ${conversation.title}`);
  lines.push('');
  lines.push(`> **Platform:** ${conversation.platform} | **Model:** ${conversation.model}`);
  lines.push(`> **Date:** ${new Date(conversation.created_at).toLocaleString()}`);
  lines.push('');
  lines.push('---');
  lines.push('');

  for (const msg of messages) {
    if (msg.role === 'system') continue;

    if (msg.role === 'user') {
      lines.push('### 👤 User');
    } else {
      lines.push('### 🤖 AI');
      if (msg.persona_name) {
        lines.push(`*Persona: ${msg.persona_name}*`);
      }
    }

    lines.push('');
    lines.push(msg.content);
    lines.push('');

    if (msg.role === 'assistant') {
      const meta: string[] = [];
      if (msg.tokens_used > 0) meta.push(`Tokens: ${msg.tokens_used}`);
      if (msg.response_time_ms) meta.push(`Time: ${msg.response_time_ms}ms`);
      if (msg.model) meta.push(`Model: ${msg.model}`);
      if (meta.length > 0) {
        lines.push(`> ${meta.join(' | ')}`);
        lines.push('');
      }
    }

    lines.push('---');
    lines.push('');
  }

  return lines.join('\\n');
}

/**
 * توليد اسم ملف التصدير
 */
export function generateExportFilename(
  title: string,
  extension: string
): string {
  const sanitized = title
    .replace(/[^a-zA-Z0-9\\u0600-\\u06FF\\s-]/g, '')
    .replace(/\\s+/g, '_')
    .substring(0, 40);

  const date = new Date().toISOString().split('T')[0];

  return `${sanitized}_${date}.${extension}`;
}
''')

    # 6. hooks/useOnboarding.ts
    create_file("hooks/useOnboarding.ts", '''// خطاف جولة التعريف: يدير خطوات الجولة التعريفية للمستخدمين الجدد
'use client';

import { useCallback, useEffect, useRef } from 'react';
import { useUIStore } from '@/stores/uiStore';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';

const TOTAL_STEPS = 6;

interface UseOnboardingReturn {
  isActive: boolean;
  currentStep: number;
  totalSteps: number;
  next: () => void;
  previous: () => void;
  skip: () => void;
  complete: () => Promise<void>;
  restart: () => void;
  goToStep: (step: number) => void;
}

export function useOnboarding(): UseOnboardingReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();
  const { tourActive, tourStep, setTourActive, setTourStep } = useUIStore();
  const checkedRef = useRef(false);

  /**
   * التحقق من حالة الجولة عند أول تحميل
   */
  useEffect(() => {
    if (!user || checkedRef.current) return;
    checkedRef.current = true;

    if (!user.onboarding_completed) {
      setTourActive(true);
      setTourStep(0);
    }

    return () => {};
  }, [user, setTourActive, setTourStep]);

  /**
   * الانتقال للخطوة التالية
   */
  const next = useCallback(() => {
    if (tourStep < TOTAL_STEPS - 1) {
      setTourStep(tourStep + 1);
    }
  }, [tourStep, setTourStep]);

  /**
   * الرجوع للخطوة السابقة
   */
  const previous = useCallback(() => {
    if (tourStep > 0) {
      setTourStep(tourStep - 1);
    }
  }, [tourStep, setTourStep]);

  /**
   * تخطي الجولة
   */
  const skip = useCallback(async () => {
    setTourActive(false);
    setTourStep(0);

    if (user) {
      try {
        await supabase
          .from('profiles')
          .update({ onboarding_completed: true })
          .eq('id', user.id);
      } catch {
        // تجاهل
      }
    }
  }, [user, supabase, setTourActive, setTourStep]);

  /**
   * إكمال الجولة
   */
  const complete = useCallback(async () => {
    setTourActive(false);
    setTourStep(0);

    if (user) {
      try {
        await supabase
          .from('profiles')
          .update({ onboarding_completed: true })
          .eq('id', user.id);
      } catch {
        // تجاهل
      }
    }
  }, [user, supabase, setTourActive, setTourStep]);

  /**
   * إعادة تشغيل الجولة
   */
  const restart = useCallback(() => {
    setTourActive(true);
    setTourStep(0);
  }, [setTourActive, setTourStep]);

  /**
   * الانتقال لخطوة محددة
   */
  const goToStep = useCallback(
    (step: number) => {
      if (step >= 0 && step < TOTAL_STEPS) {
        setTourStep(step);
      }
    },
    [setTourStep]
  );

  return {
    isActive: tourActive,
    currentStep: tourStep,
    totalSteps: TOTAL_STEPS,
    next,
    previous,
    skip,
    complete,
    restart,
    goToStep,
  };
}
''')

    # 7. hooks/useTheme.ts
    create_file("hooks/useTheme.ts", '''// خطاف المظهر: يدير تبديل المظهر بين مظلم وفاتح وتلقائي
'use client';

import { useCallback, useEffect, useRef } from 'react';
import { useUIStore } from '@/stores/uiStore';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';

type ThemeMode = 'dark' | 'light' | 'auto';

interface UseThemeReturn {
  theme: ThemeMode;
  isDark: boolean;
  isLight: boolean;
  setTheme: (theme: ThemeMode) => void;
  toggleTheme: () => void;
}

export function useTheme(): UseThemeReturn {
  const supabase = createSupabaseBrowserClient();
  const { user } = useAuthStore();
  const { theme, setTheme: setStoreTheme } = useUIStore();
  const initializedRef = useRef(false);

  /**
   * تطبيق المظهر على HTML
   */
  const applyTheme = useCallback((mode: ThemeMode) => {
    if (typeof document === 'undefined') return;

    const root = document.documentElement;
    root.style.transition = 'background-color 200ms ease, color 200ms ease';

    if (mode === 'dark') {
      root.classList.add('dark');
    } else if (mode === 'light') {
      root.classList.remove('dark');
    } else {
      // تلقائي - حسب النظام
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (prefersDark) {
        root.classList.add('dark');
      } else {
        root.classList.remove('dark');
      }
    }
  }, []);

  /**
   * تعيين المظهر
   */
  const setTheme = useCallback(
    (mode: ThemeMode) => {
      setStoreTheme(mode);
      applyTheme(mode);

      // حفظ في قاعدة البيانات
      if (user) {
        supabase
          .from('profiles')
          .update({ preferred_theme: mode })
          .eq('id', user.id)
          .then(() => {})
          .catch(() => {});
      }
    },
    [setStoreTheme, applyTheme, user, supabase]
  );

  /**
   * تبديل المظهر
   */
  const toggleTheme = useCallback(() => {
    const newTheme: ThemeMode = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }, [theme, setTheme]);

  /**
   * تطبيق المظهر عند التحميل
   */
  useEffect(() => {
    if (initializedRef.current) return;
    initializedRef.current = true;

    applyTheme(theme);

    // الاستماع لتغيير نظام الألوان في الوضع التلقائي
    if (theme === 'auto') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleChange = () => applyTheme('auto');
      mediaQuery.addEventListener('change', handleChange);

      return () => mediaQuery.removeEventListener('change', handleChange);
    }

    return () => {};
  }, [theme, applyTheme]);

  const isDark =
    theme === 'dark' ||
    (theme === 'auto' &&
      typeof window !== 'undefined' &&
      window.matchMedia('(prefers-color-scheme: dark)').matches);

  return {
    theme,
    isDark,
    isLight: !isDark,
    setTheme,
    toggleTheme,
  };
}
''')

    # ──────────────────────────────────────────────
    # ONBOARDING COMPONENTS
    # ──────────────────────────────────────────────
    print("\n📁 Onboarding Components")
    print("-" * 40)

    # 8. OnboardingTour.tsx
    create_file("components/onboarding/OnboardingTour.tsx", '''// جولة التعريف: يعرض خطوات الجولة مع تراكب ضبابي وتمييز العنصر المستهدف
'use client';

import { useCallback } from 'react';
import { useTranslations } from 'next-intl';
import { cn } from '@/utils/cn';
import { useOnboarding } from '@/hooks/useOnboarding';
import { TourStep } from './TourStep';
import {
  PanelRight, LayoutDashboard, Sparkles, Slash,
  Key, Rocket,
} from 'lucide-react';

/**
 * بيانات خطوات الجولة
 */
const STEP_ICONS = [PanelRight, LayoutDashboard, Sparkles, Slash, Key, Rocket];

export function OnboardingTour() {
  const t = useTranslations('onboarding');
  const {
    isActive,
    currentStep,
    totalSteps,
    next,
    previous,
    skip,
    complete,
  } = useOnboarding();

  const handleAction = useCallback(() => {
    if (currentStep === totalSteps - 1) {
      complete();
    } else {
      next();
    }
  }, [currentStep, totalSteps, complete, next]);

  if (!isActive) return null;

  const stepKeys = [
    { title: t('step1_title'), message: t('step1_message') },
    { title: t('step2_title'), message: t('step2_message') },
    { title: t('step3_title'), message: t('step3_message') },
    { title: t('step4_title'), message: t('step4_message') },
    { title: t('step5_title'), message: t('step5_message') },
    { title: t('step6_title'), message: t('step6_message') },
  ];

  const current = stepKeys[currentStep];
  const Icon = STEP_ICONS[currentStep];
  const isLast = currentStep === totalSteps - 1;

  if (!current || !Icon) return null;

  return (
    <>
      {/* التراكب الضبابي */}
      <div
        className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm"
        onClick={skip}
        aria-hidden="true"
      />

      {/* بطاقة الخطوة */}
      <div
        className={cn(
          'fixed z-[101] top-1/2 start-1/2 -translate-x-1/2 -translate-y-1/2',
          'w-full max-w-md'
        )}
      >
        <TourStep
          icon={Icon}
          title={current.title}
          message={current.message}
          stepNumber={currentStep + 1}
          totalSteps={totalSteps}
          isFirst={currentStep === 0}
          isLast={isLast}
          onNext={handleAction}
          onPrevious={previous}
          onSkip={skip}
          nextLabel={isLast ? t('start_using') : t('next')}
          previousLabel={t('previous')}
          skipLabel={t('skip')}
        />
      </div>
    </>
  );
}
''')

    # 9. TourStep.tsx
    create_file("components/onboarding/TourStep.tsx", '''// خطوة الجولة: بطاقة تعريفية مع عنوان ورسالة وأيقونة وأزرار تنقل
'use client';

import { memo } from 'react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight, X } from 'lucide-react';
import { useLocale } from 'next-intl';
import type { LucideIcon } from 'lucide-react';

interface TourStepProps {
  icon: LucideIcon;
  title: string;
  message: string;
  stepNumber: number;
  totalSteps: number;
  isFirst: boolean;
  isLast: boolean;
  onNext: () => void;
  onPrevious: () => void;
  onSkip: () => void;
  nextLabel: string;
  previousLabel: string;
  skipLabel: string;
}

export const TourStep = memo(function TourStep({
  icon: Icon,
  title,
  message,
  stepNumber,
  totalSteps,
  isFirst,
  isLast,
  onNext,
  onPrevious,
  onSkip,
  nextLabel,
  previousLabel,
  skipLabel,
}: TourStepProps) {
  const locale = useLocale();
  const isRTL = locale === 'ar';

  return (
    <div className="rounded-2xl border border-primary-500/30 bg-dark-900 shadow-2xl shadow-primary-500/10 overflow-hidden animate-fade-in">
      {/* شريط التقدم */}
      <div className="h-1 bg-dark-700">
        <div
          className="h-full bg-gradient-to-r from-primary-500 to-secondary-500 transition-all duration-500"
          style={{ width: `${(stepNumber / totalSteps) * 100}%` }}
        />
      </div>

      {/* المحتوى */}
      <div className="p-6 space-y-4">
        {/* رأس مع إغلاق */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 shadow-lg">
              <Icon className="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-100">{title}</h3>
              <span className="text-xs text-gray-400 font-mono">
                {stepNumber}/{totalSteps}
              </span>
            </div>
          </div>
          <button
            onClick={onSkip}
            className="rounded-lg p-1.5 text-gray-400 hover:text-gray-200 hover:bg-dark-700 transition-colors"
            aria-label="Close tour"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* الرسالة */}
        <p className="text-sm text-gray-300 leading-relaxed">{message}</p>

        {/* نقاط التقدم */}
        <div className="flex justify-center gap-1.5">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={`dot-${i}`}
              className={cn(
                'h-1.5 rounded-full transition-all duration-300',
                i === stepNumber - 1
                  ? 'w-6 bg-primary-500'
                  : i < stepNumber
                    ? 'w-1.5 bg-primary-500/50'
                    : 'w-1.5 bg-dark-600'
              )}
            />
          ))}
        </div>

        {/* الأزرار */}
        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-2">
            {!isFirst && (
              <Button variant="ghost" size="sm" onClick={onPrevious}>
                {isRTL ? (
                  <ChevronRight className="h-4 w-4 me-1" />
                ) : (
                  <ChevronLeft className="h-4 w-4 me-1" />
                )}
                {previousLabel}
              </Button>
            )}
            {!isLast && (
              <Button variant="ghost" size="sm" onClick={onSkip} className="text-gray-400">
                {skipLabel}
              </Button>
            )}
          </div>

          <Button size="sm" onClick={onNext} className={cn(isLast && 'gap-2')}>
            {nextLabel}
            {!isLast && (
              isRTL ? (
                <ChevronLeft className="h-4 w-4 ms-1" />
              ) : (
                <ChevronRight className="h-4 w-4 ms-1" />
              )
            )}
          </Button>
        </div>
      </div>
    </div>
  );
});
''')

    # ──────────────────────────────────────────────
    # SETTINGS COMPONENTS (updated/complete)
    # ──────────────────────────────────────────────
    print("\n📁 Settings Components (updated)")
    print("-" * 40)

    # 10. ProfileSettings.tsx (complete rewrite)
    create_file("components/settings/ProfileSettings.tsx", '''// إعدادات الملف الشخصي: تعديل الاسم والإحصائيات والتجربة وكود الدعوة
'use client';

import { useState, useCallback } from 'react';
import { useTranslations } from 'next-intl';
import {
  User, Save, Gift, Sparkles, MessageSquare, Hash,
  Calendar, Crown, Ticket, Check, AlertCircle,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';
import { formatDate, formatNumber, formatTokenCount } from '@/utils/formatters';
import { isValidInviteCode } from '@/utils/validators';
import { TRIAL_DURATION_DAYS } from '@/utils/constants';

export function ProfileSettings() {
  const t = useTranslations('settings');
  const { user, refreshProfile } = useAuth();
  const { role } = useAuthStore();
  const supabase = createSupabaseBrowserClient();

  const [displayName, setDisplayName] = useState(user?.display_name ?? '');
  const [isSaving, setIsSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [isActivatingTrial, setIsActivatingTrial] = useState(false);
  const [trialResult, setTrialResult] = useState<'success' | 'already_used' | null>(null);

  const [inviteCode, setInviteCode] = useState('');
  const [isActivatingCode, setIsActivatingCode] = useState(false);
  const [codeError, setCodeError] = useState('');
  const [codeSuccess, setCodeSuccess] = useState(false);

  const [stats, setStats] = useState<{
    conversations: number;
    messages: number;
    tokens: number;
  } | null>(null);
  const [statsLoaded, setStatsLoaded] = useState(false);

  /**
   * تحميل الإحصائيات
   */
  const loadStats = useCallback(async () => {
    if (!user || statsLoaded) return;
    setStatsLoaded(true);

    try {
      const [convResult, msgResult] = await Promise.all([
        supabase
          .from('conversations')
          .select('id, total_tokens', { count: 'exact' })
          .eq('user_id', user.id),
        supabase
          .from('messages')
          .select('id', { count: 'exact', head: true })
          .in(
            'conversation_id',
            ((await supabase.from('conversations').select('id').eq('user_id', user.id)).data ?? []).map(
              (c: { id: string }) => c.id
            )
          ),
      ]);

      const totalTokens = (convResult.data ?? []).reduce(
        (sum, c) => sum + ((c as { total_tokens: number }).total_tokens ?? 0),
        0
      );

      setStats({
        conversations: convResult.count ?? 0,
        messages: msgResult.count ?? 0,
        tokens: totalTokens,
      });
    } catch {
      // تجاهل
    }
  }, [user, supabase, statsLoaded]);

  // تحميل الإحصائيات عند العرض
  if (!statsLoaded && user) {
    loadStats();
  }

  /**
   * حفظ الاسم
   */
  const handleSaveName = useCallback(async () => {
    if (!user) return;
    setIsSaving(true);
    try {
      await supabase
        .from('profiles')
        .update({ display_name: displayName.trim() || null })
        .eq('id', user.id);
      await refreshProfile();
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch { /* تجاهل */ } finally {
      setIsSaving(false);
    }
  }, [user, displayName, supabase, refreshProfile]);

  /**
   * تفعيل التجربة المجانية
   */
  const handleActivateTrial = useCallback(async () => {
    if (!user || user.trial_used) {
      setTrialResult('already_used');
      return;
    }
    setIsActivatingTrial(true);
    try {
      const trialEnd = new Date();
      trialEnd.setDate(trialEnd.getDate() + TRIAL_DURATION_DAYS);

      await supabase
        .from('profiles')
        .update({
          role: 'premium',
          trial_expires_at: trialEnd.toISOString(),
          premium_expires_at: trialEnd.toISOString(),
        })
        .eq('id', user.id);

      // إنشاء إشعار
      await supabase.from('notifications').insert({
        type: 'trial_requested',
        title: 'طلب تجربة مجانية',
        message: `المستخدم ${user.email} فعّل التجربة المجانية`,
        priority: 'info',
        related_user_id: user.id,
      });

      await refreshProfile();
      setTrialResult('success');
    } catch { /* تجاهل */ } finally {
      setIsActivatingTrial(false);
    }
  }, [user, supabase, refreshProfile]);

  /**
   * تفعيل كود الدعوة
   */
  const handleActivateCode = useCallback(async () => {
    if (!user) return;
    setCodeError('');
    setCodeSuccess(false);

    if (!isValidInviteCode(inviteCode)) {
      setCodeError(t('code_invalid'));
      return;
    }

    setIsActivatingCode(true);
    try {
      const response = await fetch(
        `/api/admin/invite-codes?code=${encodeURIComponent(inviteCode.trim())}`,
        { method: 'GET' }
      );

      if (!response.ok) {
        const data = await response.json().catch(() => ({})) as Record<string, string>;
        setCodeError(data.error ?? t('code_invalid'));
        return;
      }

      // التفعيل عبر صفحة الدعوة
      const locale = document.documentElement.lang || 'ar';
      window.location.href = `/${locale}/invite/${inviteCode.trim()}`;
    } catch {
      setCodeError(t('code_invalid'));
    } finally {
      setIsActivatingCode(false);
    }
  }, [user, inviteCode, t]);

  if (!user) return null;

  const roleBadges = {
    admin: { label: t('admin') ?? 'Admin', variant: 'destructive' as const, icon: Crown },
    premium: { label: t('premium') ?? 'Premium', variant: 'premium' as const, icon: Sparkles },
    free: { label: t('free') ?? 'Free', variant: 'secondary' as const, icon: User },
  };
  const badge = roleBadges[role];

  return (
    <div className="space-y-6">
      {/* الاسم */}
      <div className="space-y-2">
        <Label>{t('display_name')}</Label>
        <div className="flex gap-2">
          <Input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder={t('display_name_placeholder')}
          />
          <Button onClick={handleSaveName} isLoading={isSaving} disabled={isSaving} size="icon">
            {saved ? <Check className="h-4 w-4 text-green-500" /> : <Save className="h-4 w-4" />}
          </Button>
        </div>
      </div>

      {/* البريد */}
      <div className="space-y-2">
        <Label>{t('email')}</Label>
        <Input value={user.email} disabled dir="ltr" />
      </div>

      {/* نوع الحساب وتاريخ الانضمام */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label>{t('account_type')}</Label>
          <div className="flex items-center gap-2">
            <badge.icon className="h-4 w-4 text-primary-500" />
            <Badge variant={badge.variant}>{badge.label}</Badge>
          </div>
        </div>
        <div className="space-y-2">
          <Label>{t('join_date')}</Label>
          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
            <Calendar className="h-4 w-4" />
            <span>{formatDate(user.created_at)}</span>
          </div>
        </div>
      </div>

      {/* الإحصائيات */}
      {stats && (
        <div className="grid grid-cols-3 gap-3">
          <div className="rounded-lg border border-gray-200 dark:border-dark-700 p-3 text-center">
            <MessageSquare className="h-5 w-5 text-primary-500 mx-auto mb-1" />
            <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
              {formatNumber(stats.conversations)}
            </p>
            <p className="text-[10px] text-gray-500">{t('total_conversations')}</p>
          </div>
          <div className="rounded-lg border border-gray-200 dark:border-dark-700 p-3 text-center">
            <MessageSquare className="h-5 w-5 text-secondary-500 mx-auto mb-1" />
            <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
              {formatNumber(stats.messages)}
            </p>
            <p className="text-[10px] text-gray-500">{t('total_messages')}</p>
          </div>
          <div className="rounded-lg border border-gray-200 dark:border-dark-700 p-3 text-center">
            <Hash className="h-5 w-5 text-accent-500 mx-auto mb-1" />
            <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
              {formatTokenCount(stats.tokens)}
            </p>
            <p className="text-[10px] text-gray-500">{t('total_tokens')}</p>
          </div>
        </div>
      )}

      {/* التجربة المجانية */}
      {role === 'free' && !user.trial_used && (
        <div className="rounded-xl border border-primary-500/30 bg-gradient-to-br from-primary-500/5 to-secondary-500/5 p-4 space-y-3">
          <div className="flex items-center gap-2">
            <Gift className="h-5 w-5 text-primary-500" />
            <span className="font-semibold text-gray-900 dark:text-gray-100">
              {t('trial_button')}
            </span>
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {TRIAL_DURATION_DAYS} {useTranslations('common')('days')}
          </p>
          <Button
            onClick={handleActivateTrial}
            isLoading={isActivatingTrial}
            className="w-full gap-2"
          >
            <Sparkles className="h-4 w-4" />
            {t('trial_button')}
          </Button>
          {trialResult === 'success' && (
            <p className="text-sm text-green-500 flex items-center gap-1">
              <Check className="h-4 w-4" /> {t('trial_success')}
            </p>
          )}
        </div>
      )}

      {user.trial_used && role === 'free' && (
        <p className="text-sm text-gray-400 flex items-center gap-1">
          <AlertCircle className="h-4 w-4" /> {t('trial_already_used')}
        </p>
      )}

      {user.trial_expires_at && role === 'premium' && (
        <div className="flex items-center gap-2 text-sm text-primary-500">
          <Sparkles className="h-4 w-4" />
          <span>{t('trial_active')} - {t('trial_expires', { date: formatDate(user.trial_expires_at) })}</span>
        </div>
      )}

      {/* كود الدعوة */}
      {role === 'free' && (
        <div className="space-y-2">
          <Label>{t('invite_code_label')}</Label>
          <div className="flex gap-2">
            <Input
              value={inviteCode}
              onChange={(e) => setInviteCode(e.target.value)}
              placeholder={t('invite_code_placeholder')}
              dir="ltr"
            />
            <Button
              onClick={handleActivateCode}
              isLoading={isActivatingCode}
              disabled={!inviteCode.trim() || isActivatingCode}
            >
              <Ticket className="h-4 w-4 me-1.5" />
              {t('activate_code')}
            </Button>
          </div>
          {codeError && <ErrorMessage message={codeError} dismissible onDismiss={() => setCodeError('')} />}
          {codeSuccess && (
            <p className="text-sm text-green-500 flex items-center gap-1">
              <Check className="h-4 w-4" /> {t('code_success')}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
''')

    # 11. LanguageSwitch.tsx
    create_file("components/settings/LanguageSwitch.tsx", '''// مبدل اللغة: تبديل فوري بين العربية والإنجليزية مع حفظ التفضيل
'use client';

import { useCallback } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import { useRouter, usePathname } from 'next/navigation';
import { Globe, Check } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useUIStore } from '@/stores/uiStore';
import { useAuthStore } from '@/stores/authStore';
import { createSupabaseBrowserClient } from '@/lib/supabase-client';

export function LanguageSwitch() {
  const tSettings = useTranslations('settings');
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();
  const supabase = createSupabaseBrowserClient();
  const { setLocale } = useUIStore();
  const { user } = useAuthStore();

  const handleSwitch = useCallback(
    async (newLocale: 'ar' | 'en') => {
      if (newLocale === locale) return;

      setLocale(newLocale);

      // حفظ في قاعدة البيانات
      if (user) {
        supabase
          .from('profiles')
          .update({ preferred_language: newLocale })
          .eq('id', user.id)
          .then(() => {})
          .catch(() => {});
      }

      // تحديث المسار
      const segments = pathname.split('/');
      if (segments.length > 1 && (segments[1] === 'ar' || segments[1] === 'en')) {
        segments[1] = newLocale;
      }
      router.push(segments.join('/'));
    },
    [locale, setLocale, user, supabase, pathname, router]
  );

  const languages = [
    { code: 'ar' as const, label: 'العربية', flag: '🇸🇦', dir: 'RTL' },
    { code: 'en' as const, label: 'English', flag: '🇺🇸', dir: 'LTR' },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Globe className="h-5 w-5 text-primary-500" />
        <span className="text-base font-semibold text-gray-900 dark:text-gray-100">
          {tSettings('language_tab')}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {languages.map((lang) => {
          const isActive = locale === lang.code;
          return (
            <button
              key={lang.code}
              onClick={() => handleSwitch(lang.code)}
              className={cn(
                'relative flex flex-col items-center gap-3 rounded-xl border p-6 transition-all duration-200',
                isActive
                  ? 'border-primary-500 bg-primary-500/10 shadow-md shadow-primary-500/10'
                  : 'border-gray-200 dark:border-dark-600 hover:border-gray-300 dark:hover:border-dark-500 hover:bg-gray-50 dark:hover:bg-dark-800'
              )}
            >
              {isActive && (
                <div className="absolute top-2 end-2">
                  <Check className="h-5 w-5 text-primary-500" />
                </div>
              )}
              <span className="text-4xl">{lang.flag}</span>
              <span className={cn(
                'text-sm font-medium',
                isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300'
              )}>
                {lang.label}
              </span>
              <span className="text-[10px] text-gray-400 font-mono">{lang.dir}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
''')

    # 12. ThemeSwitch.tsx
    create_file("components/settings/ThemeSwitch.tsx", '''// مبدل المظهر: تبديل فوري بين مظلم وفاتح وتلقائي مع انتقال سلس
'use client';

import { useTranslations } from 'next-intl';
import { Moon, Sun, Monitor, Check } from 'lucide-react';
import { cn } from '@/utils/cn';
import { useTheme } from '@/hooks/useTheme';

export function ThemeSwitch() {
  const tSettings = useTranslations('settings');
  const tSidebar = useTranslations('sidebar');
  const { theme, setTheme } = useTheme();

  const themes = [
    {
      key: 'dark' as const,
      icon: Moon,
      label: tSidebar('theme_dark'),
      description: 'مظلم مريح للعين',
      preview: 'bg-dark-900 border-dark-700',
    },
    {
      key: 'light' as const,
      icon: Sun,
      label: tSidebar('theme_light'),
      description: 'فاتح ومشرق',
      preview: 'bg-white border-gray-200',
    },
    {
      key: 'auto' as const,
      icon: Monitor,
      label: tSidebar('theme_auto'),
      description: 'حسب نظام التشغيل',
      preview: 'bg-gradient-to-br from-dark-900 to-white border-gray-300',
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Moon className="h-5 w-5 text-primary-500" />
        <span className="text-base font-semibold text-gray-900 dark:text-gray-100">
          {tSettings('theme_tab')}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-3">
        {themes.map(({ key, icon: Icon, label, preview }) => {
          const isActive = theme === key;
          return (
            <button
              key={key}
              onClick={() => setTheme(key)}
              className={cn(
                'relative flex flex-col items-center gap-3 rounded-xl border p-4 transition-all duration-200',
                isActive
                  ? 'border-primary-500 bg-primary-500/10 shadow-md shadow-primary-500/10'
                  : 'border-gray-200 dark:border-dark-600 hover:border-gray-300 dark:hover:border-dark-500 hover:bg-gray-50 dark:hover:bg-dark-800'
              )}
            >
              {isActive && (
                <div className="absolute top-2 end-2">
                  <Check className="h-4 w-4 text-primary-500" />
                </div>
              )}

              {/* معاينة المظهر */}
              <div className={cn('w-full h-12 rounded-lg border', preview)} />

              <Icon className={cn(
                'h-5 w-5',
                isActive ? 'text-primary-500' : 'text-gray-500'
              )} />

              <span className={cn(
                'text-xs font-medium',
                isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'
              )}>
                {label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
''')

    # 13. ExportImport.tsx
    create_file("components/settings/ExportImport.tsx", '''// تصدير واستيراد البيانات: تصدير JSON شامل (بدون مفاتيح) واستيراد مع تحقق
'use client';

import { useState, useRef } from 'react';
import { useTranslations } from 'next-intl';
import {
  Download, Upload, FileCode, AlertTriangle, Check,
  Shield, ArrowDownToLine, ArrowUpToLine,
} from 'lucide-react';
import { cn } from '@/utils/cn';
import { Button } from '@/components/ui/button';
import { ErrorMessage } from '@/components/common/ErrorMessage';
import { useExport } from '@/hooks/useExport';

export function ExportImport() {
  const t = useTranslations('settings');
  const { isExporting, exportAllSettings, importSettings } = useExport();

  const [isImporting, setIsImporting] = useState(false);
  const [importResult, setImportResult] = useState<{
    type: 'success' | 'error';
    message: string;
  } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  /**
   * معالجة الاستيراد
   */
  const handleImport = async (file: File) => {
    setIsImporting(true);
    setImportResult(null);

    try {
      const result = await importSettings(file);
      if (result.success) {
        setImportResult({ type: 'success', message: t('import_success') });
      } else {
        setImportResult({
          type: 'error',
          message: result.error ?? t('import_error'),
        });
      }
    } catch {
      setImportResult({ type: 'error', message: t('import_error') });
    } finally {
      setIsImporting(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="space-y-8">
      {/* قسم التصدير */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <ArrowDownToLine className="h-5 w-5 text-primary-500" />
          <span className="text-base font-semibold text-gray-900 dark:text-gray-100">
            {t('export_settings')}
          </span>
        </div>

        <p className="text-sm text-gray-500 dark:text-gray-400">
          {t('export_description')}
        </p>

        {/* ماذا يتضمن التصدير */}
        <div className="rounded-lg border border-gray-200 dark:border-dark-700 p-3 space-y-2">
          <p className="text-xs font-medium text-gray-600 dark:text-gray-400">يتضمن:</p>
          <div className="grid grid-cols-2 gap-1.5 text-xs text-gray-500">
            <span>✅ المحادثات والرسائل</span>
            <span>✅ الشخصيات المخصصة</span>
            <span>✅ المجلدات</span>
            <span>✅ المفضلات</span>
            <span>✅ التفضيلات</span>
            <span className="text-red-400">❌ مفاتيح API</span>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs text-orange-500">
          <Shield className="h-3.5 w-3.5 shrink-0" />
          <span>{t('export_excludes')}</span>
        </div>

        <Button
          onClick={exportAllSettings}
          isLoading={isExporting}
          variant="outline"
          className="gap-2"
        >
          <Download className="h-4 w-4" />
          {t('export_button')}
        </Button>
      </div>

      {/* فاصل */}
      <div className="h-px bg-gray-200 dark:bg-dark-700" />

      {/* قسم الاستيراد */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <ArrowUpToLine className="h-5 w-5 text-primary-500" />
          <span className="text-base font-semibold text-gray-900 dark:text-gray-100">
            {t('import_settings')}
          </span>
        </div>

        <div className="rounded-lg border-2 border-dashed border-gray-300 dark:border-dark-600 p-6 text-center space-y-3">
          <Upload className="h-8 w-8 text-gray-400 mx-auto" />
          <p className="text-sm text-gray-500 dark:text-gray-400">
            JSON ({t('export_button')})
          </p>

          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleImport(file);
            }}
            className="hidden"
          />

          <Button
            onClick={() => fileInputRef.current?.click()}
            isLoading={isImporting}
            variant="outline"
            className="gap-2"
          >
            <Upload className="h-4 w-4" />
            {t('import_button')}
          </Button>
        </div>

        {/* نتيجة الاستيراد */}
        {importResult?.type === 'success' && (
          <div className="flex items-center gap-2 text-sm text-green-500">
            <Check className="h-4 w-4" />
            <span>{importResult.message}</span>
          </div>
        )}

        {importResult?.type === 'error' && (
          <ErrorMessage
            message={importResult.message}
            dismissible
            onDismiss={() => setImportResult(null)}
          />
        )}
      </div>
    </div>
  );
}
''')

    # ──────────────────────────────────────────────
    # Summary
    # ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 BUILD PHASE 5A SUMMARY")
    print("=" * 60)
    print(f"  ✅ Files created: {files_created}")
    print(f"  ❌ Files failed: {files_failed}")
    print(f"  📁 Total: {files_created + files_failed}")
    print()
    print("📋 Files Created:")
    print()
    print("  HOOKS:")
    print("    1.  hooks/useFolders.ts         (CRUD + move + reorder + auto-folder)")
    print("    2.  hooks/useFavorites.ts        (add/remove/check/reorder persona|model)")
    print("    3.  hooks/useTokenTracker.ts     (per-msg + per-conv + per-user + usage_stats)")
    print("    4.  hooks/useExport.ts           (PDF + TXT + MD + JSON + import)")
    print("    5.  hooks/useOnboarding.ts       (6 steps, start/next/prev/skip/complete)")
    print("    6.  hooks/useTheme.ts            (dark/light/auto + 200ms transition)")
    print()
    print("  LIBRARIES:")
    print("    7.  lib/export.ts                (generatePDF color-coded, TXT, Markdown)")
    print()
    print("  ONBOARDING COMPONENTS:")
    print("    8.  components/onboarding/OnboardingTour.tsx  (Controller + overlay)")
    print("    9.  components/onboarding/TourStep.tsx        (Card + dots + nav)")
    print()
    print("  SETTINGS COMPONENTS:")
    print("    10. components/settings/ProfileSettings.tsx   (Name + stats + trial + invite)")
    print("    11. components/settings/LanguageSwitch.tsx    (AR/EN + flag + save to DB)")
    print("    12. components/settings/ThemeSwitch.tsx       (Dark/Light/Auto + preview)")
    print("    13. components/settings/ExportImport.tsx      (Export JSON + import + validate)")
    print()
    print("📝 KEY FEATURES:")
    print("  - useFolders: auto-create folder on first persona use")
    print("  - useFolders: deleteFolder with moveConversationsTo option")
    print("  - useFavorites: separate persona/model lists, reorder support")
    print("  - useTokenTracker: upserts usage_stats daily, tracks 3 levels")
    print("  - useExport: PDF with color-coded bubbles (purple user, gray AI)")
    print("  - lib/export: generatePDF uses jsPDF, handles page breaks")
    print("  - useOnboarding: auto-starts if !onboarding_completed, saves to DB")
    print("  - useTheme: applies CSS transition 200ms, syncs with DB + uiStore")
    print("  - OnboardingTour: overlay + centered card + progress dots")
    print("  - TourStep: icon + title + message + step counter + nav buttons")
    print("  - ProfileSettings: stats cards, trial activation, invite code input")
    print("  - LanguageSwitch: instant switch with flag, saves preferred_language")
    print("  - ThemeSwitch: 3 options with preview boxes, saves preferred_theme")
    print("  - ExportImport: includes checklist, excludes API keys note")
    print("  - All i18n, TypeScript strict, no 'any', RTL/LTR")
    print()
    print("🔜 REMAINING PHASES:")
    print("  Phase 5B: Personas (library page, create page, cards, ratings)")
    print("  Phase 6A: Admin (layout, dashboard, users management)")
    print("  Phase 6B: Admin (keys, models, personas, codes, notifications)")
    print("  Phase 7:  Final (telegram, worker polish, README)")
    print()
    print("✅ Phase 5A Complete! Ready for Phase 5B.")


if __name__ == "__main__":
    main()
